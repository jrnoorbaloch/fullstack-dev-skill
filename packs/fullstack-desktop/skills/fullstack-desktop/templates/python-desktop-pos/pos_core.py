"""Business logic for the POS: products, stock, sales, reports. No UI code here, so it is easy to test."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    barcode TEXT UNIQUE,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    low_stock_at INTEGER NOT NULL DEFAULT 5
);
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    subtotal REAL NOT NULL,
    discount REAL NOT NULL DEFAULT 0,
    tax REAL NOT NULL DEFAULT 0,
    total REAL NOT NULL,
    paid REAL NOT NULL,
    change REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    name TEXT NOT NULL,
    qty INTEGER NOT NULL CHECK (qty > 0),
    price REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sales_created ON sales(created_at);
"""


class POSError(Exception):
    """Raised for user-facing errors (out of stock, unknown product, etc.)."""


@dataclass
class CartLine:
    product_id: int
    name: str
    price: float
    qty: int

    @property
    def total(self) -> float:
        return round(self.price * self.qty, 2)


class POS:
    def __init__(self, db_path: str | Path = "pos.db", tax_rate: float = 0.0):
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)
        self.tax_rate = tax_rate
        self.cart: dict[int, CartLine] = {}

    # ---------- products ----------
    def add_product(self, name: str, price: float, stock: int = 0, barcode: str | None = None, low_stock_at: int = 5) -> int:
        name = name.strip()
        if not name:
            raise POSError("Product name is required")
        if price < 0 or stock < 0:
            raise POSError("Price and stock cannot be negative")
        try:
            cur = self.conn.execute(
                "INSERT INTO products (barcode, name, price, stock, low_stock_at) VALUES (?, ?, ?, ?, ?)",
                (barcode or None, name, price, stock, low_stock_at),
            )
        except sqlite3.IntegrityError as e:
            raise POSError("Barcode already exists") from e
        self.conn.commit()
        return cur.lastrowid

    def update_stock(self, product_id: int, delta: int) -> None:
        row = self.conn.execute("SELECT stock FROM products WHERE id = ?", (product_id,)).fetchone()
        if not row:
            raise POSError("Product not found")
        if row["stock"] + delta < 0:
            raise POSError("Stock cannot go below zero")
        self.conn.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (delta, product_id))
        self.conn.commit()

    def find_product(self, query: str) -> sqlite3.Row | None:
        query = query.strip()
        row = self.conn.execute("SELECT * FROM products WHERE barcode = ?", (query,)).fetchone()
        if row:
            return row
        if query.isdigit():
            row = self.conn.execute("SELECT * FROM products WHERE id = ?", (int(query),)).fetchone()
            if row:
                return row
        return self.conn.execute("SELECT * FROM products WHERE name LIKE ? ORDER BY name LIMIT 1", (f"%{query}%",)).fetchone()

    def list_products(self, search: str = "") -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM products WHERE name LIKE ? OR barcode LIKE ? ORDER BY name", (f"%{search}%", f"%{search}%")
        ).fetchall()

    def low_stock(self) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM products WHERE stock <= low_stock_at ORDER BY stock").fetchall()

    # ---------- cart ----------
    def add_to_cart(self, query: str, qty: int = 1) -> CartLine:
        if qty <= 0:
            raise POSError("Quantity must be positive")
        p = self.find_product(query)
        if not p:
            raise POSError(f"No product matches '{query}'")
        in_cart = self.cart[p["id"]].qty if p["id"] in self.cart else 0
        if in_cart + qty > p["stock"]:
            raise POSError(f"Only {p['stock']} of {p['name']} in stock")
        line = self.cart.setdefault(p["id"], CartLine(p["id"], p["name"], p["price"], 0))
        line.qty += qty
        return line

    def remove_from_cart(self, product_id: int) -> None:
        self.cart.pop(product_id, None)

    def totals(self, discount: float = 0.0) -> dict[str, float]:
        subtotal = round(sum(l.total for l in self.cart.values()), 2)
        discount = min(max(discount, 0.0), subtotal)
        tax = round((subtotal - discount) * self.tax_rate, 2)
        return {"subtotal": subtotal, "discount": round(discount, 2), "tax": tax, "total": round(subtotal - discount + tax, 2)}

    def checkout(self, paid: float, discount: float = 0.0) -> int:
        if not self.cart:
            raise POSError("Cart is empty")
        t = self.totals(discount)
        if paid < t["total"]:
            raise POSError(f"Paid amount is less than total ({t['total']:.2f})")
        change = round(paid - t["total"], 2)
        with self.conn:  # one transaction: sale + items + stock
            cur = self.conn.execute(
                "INSERT INTO sales (created_at, subtotal, discount, tax, total, paid, change) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (datetime.now().isoformat(timespec="seconds"), t["subtotal"], t["discount"], t["tax"], t["total"], paid, change),
            )
            sale_id = cur.lastrowid
            for l in self.cart.values():
                self.conn.execute(
                    "INSERT INTO sale_items (sale_id, product_id, name, qty, price) VALUES (?, ?, ?, ?, ?)",
                    (sale_id, l.product_id, l.name, l.qty, l.price),
                )
                updated = self.conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?", (l.qty, l.product_id, l.qty)
                ).rowcount
                if not updated:
                    raise POSError(f"Not enough stock for {l.name}")
        self.cart.clear()
        return sale_id

    # ---------- receipts & reports ----------
    def receipt_text(self, sale_id: int, shop_name: str = "My Shop", width: int = 32) -> str:
        sale = self.conn.execute("SELECT * FROM sales WHERE id = ?", (sale_id,)).fetchone()
        if not sale:
            raise POSError("Sale not found")
        items = self.conn.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,)).fetchall()
        line = "-" * width
        out = [shop_name.center(width), f"Receipt #{sale_id}".center(width), sale["created_at"].replace("T", " ").center(width), line]
        for it in items:
            out.append(it["name"][:width])
            amount = f"{it['qty']} x {it['price']:.2f}"
            out.append(f"{amount}{it['qty'] * it['price']:>{width - len(amount)}.2f}")
        out.append(line)
        for label in ("subtotal", "discount", "tax", "total", "paid", "change"):
            if label in ("discount", "tax") and not sale[label]:
                continue
            text = label.capitalize()
            out.append(f"{text}{sale[label]:>{width - len(text)}.2f}")
        out += [line, "Thank you!".center(width)]
        return "\n".join(out)

    def daily_report(self, day: date | None = None) -> dict:
        day = day or date.today()
        row = self.conn.execute(
            "SELECT COUNT(*) AS sales, COALESCE(SUM(total), 0) AS revenue FROM sales WHERE substr(created_at, 1, 10) = ?",
            (day.isoformat(),),
        ).fetchone()
        top = self.conn.execute(
            """SELECT si.name, SUM(si.qty) AS qty FROM sale_items si JOIN sales s ON s.id = si.sale_id
               WHERE substr(s.created_at, 1, 10) = ? GROUP BY si.name ORDER BY qty DESC LIMIT 5""",
            (day.isoformat(),),
        ).fetchall()
        return {"date": day.isoformat(), "sales": row["sales"], "revenue": round(row["revenue"], 2), "top_items": [dict(r) for r in top]}

    def export_sales_csv(self, path: str | Path) -> Path:
        import csv

        path = Path(path)
        rows = self.conn.execute("SELECT * FROM sales ORDER BY created_at").fetchall()
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "created_at", "subtotal", "discount", "tax", "total", "paid", "change"])
            w.writerows([tuple(r) for r in rows])
        return path
