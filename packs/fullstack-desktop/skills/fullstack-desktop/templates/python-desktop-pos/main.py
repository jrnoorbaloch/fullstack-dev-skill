"""Tkinter POS desktop app. Run: python main.py"""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from pos_core import POS, POSError

APP_DIR = Path.home() / ".simple-pos"
APP_DIR.mkdir(exist_ok=True)
SHOP_NAME = "My Shop"
TAX_RATE = 0.0  # e.g. 0.17 for 17%


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{SHOP_NAME} — POS")
        self.geometry("1000x620")
        self.minsize(820, 520)
        self.pos = POS(APP_DIR / "pos.db", tax_rate=TAX_RATE)
        if not self.pos.list_products():
            for name, price, stock, code in [("Tea", 80, 50, "1001"), ("Biscuits", 50, 40, "1002"), ("Water 1.5L", 100, 30, "1003")]:
                self.pos.add_product(name, price, stock, code)

        style = ttk.Style(self)
        style.configure("Total.TLabel", font=("Segoe UI", 20, "bold"))

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)
        self.sale_tab = ttk.Frame(nb, padding=8)
        self.products_tab = ttk.Frame(nb, padding=8)
        self.reports_tab = ttk.Frame(nb, padding=8)
        nb.add(self.sale_tab, text="  Sale  ")
        nb.add(self.products_tab, text="  Products  ")
        nb.add(self.reports_tab, text="  Reports  ")
        nb.bind("<<NotebookTabChanged>>", lambda _e: (self.refresh_products(), self.refresh_report()))

        self.build_sale_tab()
        self.build_products_tab()
        self.build_reports_tab()
        self.after(300, self.warn_low_stock)

    # ---------------- Sale ----------------
    def build_sale_tab(self) -> None:
        top = ttk.Frame(self.sale_tab)
        top.pack(fill="x")
        ttk.Label(top, text="Barcode / name:").pack(side="left")
        self.scan_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.scan_var, width=30)
        entry.pack(side="left", padx=6)
        entry.bind("<Return>", lambda _e: self.scan())
        entry.focus()
        ttk.Label(top, text="Qty:").pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(top, from_=1, to=999, textvariable=self.qty_var, width=5).pack(side="left", padx=6)
        ttk.Button(top, text="Add", command=self.scan).pack(side="left")

        cols = ("name", "qty", "price", "total")
        self.cart_tree = ttk.Treeview(self.sale_tab, columns=cols, show="headings", height=14)
        for c, w in zip(cols, (380, 80, 120, 120)):
            self.cart_tree.heading(c, text=c.capitalize())
            self.cart_tree.column(c, width=w, anchor="w" if c == "name" else "e")
        self.cart_tree.pack(fill="both", expand=True, pady=8)
        self.cart_tree.bind("<Delete>", lambda _e: self.remove_selected())

        bottom = ttk.Frame(self.sale_tab)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Remove selected (Del)", command=self.remove_selected).pack(side="left")
        ttk.Label(bottom, text="Discount:").pack(side="left", padx=(16, 4))
        self.discount_var = tk.DoubleVar(value=0)
        disc = ttk.Entry(bottom, textvariable=self.discount_var, width=8)
        disc.pack(side="left")
        disc.bind("<KeyRelease>", lambda _e: self.refresh_cart())
        self.total_label = ttk.Label(bottom, text="Total: 0.00", style="Total.TLabel")
        self.total_label.pack(side="right")
        ttk.Button(bottom, text="Checkout (F12)", command=self.checkout).pack(side="right", padx=12)
        self.bind("<F12>", lambda _e: self.checkout())

    def discount(self) -> float:
        try:
            return float(self.discount_var.get())
        except (tk.TclError, ValueError):
            return 0.0

    def scan(self) -> None:
        q = self.scan_var.get().strip()
        if not q:
            return
        try:
            self.pos.add_to_cart(q, int(self.qty_var.get()))
        except (POSError, tk.TclError, ValueError) as e:
            messagebox.showwarning("Cannot add", str(e))
        self.scan_var.set("")
        self.qty_var.set(1)
        self.refresh_cart()

    def remove_selected(self) -> None:
        for iid in self.cart_tree.selection():
            self.pos.remove_from_cart(int(iid))
        self.refresh_cart()

    def refresh_cart(self) -> None:
        self.cart_tree.delete(*self.cart_tree.get_children())
        for pid, l in self.pos.cart.items():
            self.cart_tree.insert("", "end", iid=str(pid), values=(l.name, l.qty, f"{l.price:.2f}", f"{l.total:.2f}"))
        self.total_label.config(text=f"Total: {self.pos.totals(self.discount())['total']:.2f}")

    def checkout(self) -> None:
        if not self.pos.cart:
            messagebox.showinfo("Checkout", "Cart is empty.")
            return
        total = self.pos.totals(self.discount())["total"]
        paid = simpledialog.askfloat("Payment", f"Total: {total:.2f}\nAmount received:", minvalue=0, parent=self)
        if paid is None:
            return
        try:
            sale_id = self.pos.checkout(paid, self.discount())
        except POSError as e:
            messagebox.showerror("Checkout failed", str(e))
            return
        receipt = self.pos.receipt_text(sale_id, SHOP_NAME)
        self.discount_var.set(0)
        self.refresh_cart()
        self.show_receipt(receipt, sale_id)
        self.warn_low_stock()

    def show_receipt(self, text: str, sale_id: int) -> None:
        win = tk.Toplevel(self)
        win.title(f"Receipt #{sale_id}")
        box = tk.Text(win, width=36, height=24, font=("Courier New", 10))
        box.insert("1.0", text)
        box.config(state="disabled")
        box.pack(padx=8, pady=8)

        def save() -> None:
            path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"receipt-{sale_id}.txt")
            if path:
                Path(path).write_text(text, encoding="utf-8")

        ttk.Button(win, text="Save / print (.txt)", command=save).pack(pady=(0, 8))

    # ---------------- Products ----------------
    def build_products_tab(self) -> None:
        bar = ttk.Frame(self.products_tab)
        bar.pack(fill="x")
        self.search_var = tk.StringVar()
        ttk.Label(bar, text="Search:").pack(side="left")
        s = ttk.Entry(bar, textvariable=self.search_var, width=30)
        s.pack(side="left", padx=6)
        s.bind("<KeyRelease>", lambda _e: self.refresh_products())
        ttk.Button(bar, text="New product", command=self.new_product).pack(side="right")
        ttk.Button(bar, text="Add stock", command=self.add_stock).pack(side="right", padx=6)

        cols = ("id", "barcode", "name", "price", "stock")
        self.prod_tree = ttk.Treeview(self.products_tab, columns=cols, show="headings")
        for c, w in zip(cols, (60, 140, 360, 120, 100)):
            self.prod_tree.heading(c, text=c.capitalize())
            self.prod_tree.column(c, width=w)
        self.prod_tree.tag_configure("low", foreground="#b91c1c")
        self.prod_tree.pack(fill="both", expand=True, pady=8)

    def refresh_products(self) -> None:
        self.prod_tree.delete(*self.prod_tree.get_children())
        for p in self.pos.list_products(self.search_var.get()):
            tag = ("low",) if p["stock"] <= p["low_stock_at"] else ()
            self.prod_tree.insert("", "end", iid=str(p["id"]), values=(p["id"], p["barcode"] or "", p["name"], f"{p['price']:.2f}", p["stock"]), tags=tag)

    def new_product(self) -> None:
        name = simpledialog.askstring("New product", "Name:", parent=self)
        if not name:
            return
        price = simpledialog.askfloat("New product", "Price:", minvalue=0, parent=self)
        if price is None:
            return
        stock = simpledialog.askinteger("New product", "Opening stock:", minvalue=0, initialvalue=0, parent=self) or 0
        barcode = simpledialog.askstring("New product", "Barcode (optional):", parent=self)
        try:
            self.pos.add_product(name, price, stock, barcode)
        except POSError as e:
            messagebox.showerror("Error", str(e))
        self.refresh_products()

    def add_stock(self) -> None:
        sel = self.prod_tree.selection()
        if not sel:
            messagebox.showinfo("Add stock", "Select a product first.")
            return
        qty = simpledialog.askinteger("Add stock", "Quantity to add:", minvalue=1, parent=self)
        if qty:
            self.pos.update_stock(int(sel[0]), qty)
            self.refresh_products()

    # ---------------- Reports ----------------
    def build_reports_tab(self) -> None:
        self.report_text = tk.Text(self.reports_tab, height=14, font=("Segoe UI", 11))
        self.report_text.pack(fill="both", expand=True)
        ttk.Button(self.reports_tab, text="Export all sales (CSV)", command=self.export_csv).pack(pady=8, anchor="e")

    def refresh_report(self) -> None:
        r = self.pos.daily_report()
        lines = [f"Today ({r['date']})", f"Sales: {r['sales']}", f"Revenue: {r['revenue']:.2f}", "", "Top items:"]
        lines += [f"  {t['name']}: {t['qty']}" for t in r["top_items"]] or ["  —"]
        low = self.pos.low_stock()
        lines += ["", "Low stock:"] + ([f"  {p['name']}: {p['stock']}" for p in low] or ["  —"])
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", "\n".join(lines))
        self.report_text.config(state="disabled")

    def export_csv(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="sales.csv")
        if path:
            self.pos.export_sales_csv(path)
            messagebox.showinfo("Export", f"Saved to {path}")

    def warn_low_stock(self) -> None:
        low = self.pos.low_stock()
        if low:
            names = ", ".join(f"{p['name']} ({p['stock']})" for p in low[:5])
            self.title(f"{SHOP_NAME} — POS   ⚠ Low stock: {names}")
        else:
            self.title(f"{SHOP_NAME} — POS")


if __name__ == "__main__":
    App().mainloop()
