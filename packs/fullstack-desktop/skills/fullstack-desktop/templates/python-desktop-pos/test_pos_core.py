import pytest

from pos_core import POS, POSError


@pytest.fixture
def pos(tmp_path):
    p = POS(tmp_path / "t.db", tax_rate=0.1)
    p.add_product("Tea", 80, 10, "1001")
    p.add_product("Biscuits", 50, 2, "1002", low_stock_at=3)
    return p


def test_sale_flow_updates_stock_and_report(pos):
    pos.add_to_cart("1001", 2)
    pos.add_to_cart("Biscuits", 1)
    t = pos.totals(discount=10)
    assert t == {"subtotal": 210.0, "discount": 10.0, "tax": 20.0, "total": 220.0}
    sale_id = pos.checkout(paid=300, discount=10)
    assert pos.find_product("1001")["stock"] == 8
    receipt = pos.receipt_text(sale_id)
    assert "Total" in receipt and "220.00" in receipt and "80.00" in receipt
    r = pos.daily_report()
    assert r["sales"] == 1 and r["revenue"] == 220.0


def test_cannot_oversell(pos):
    with pytest.raises(POSError):
        pos.add_to_cart("1002", 3)


def test_underpayment_rejected(pos):
    pos.add_to_cart("1001")
    with pytest.raises(POSError):
        pos.checkout(paid=1)
    assert pos.cart  # cart kept


def test_low_stock_and_duplicate_barcode(pos):
    assert [p["name"] for p in pos.low_stock()] == ["Biscuits"]
    with pytest.raises(POSError):
        pos.add_product("Other", 1, 1, "1001")


def test_export_csv(pos, tmp_path):
    pos.add_to_cart("Tea")
    pos.checkout(paid=100)
    out = pos.export_sales_csv(tmp_path / "s.csv")
    assert out.read_text().count("\n") == 2
