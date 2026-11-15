# Simple POS (Python desktop)

Offline point-of-sale for small shops: barcode/name search, cart, discount, tax, checkout with change, receipts, stock with low-stock alerts, daily report, CSV export. Uses only the Python standard library (Tkinter + SQLite).

## Run
```bash
python main.py
```
Data is stored in `~/.simple-pos/pos.db`. Set `SHOP_NAME` and `TAX_RATE` at the top of `main.py`.

Shortcuts: **Enter** adds the scanned item · **Del** removes a cart line · **F12** checkout. USB barcode scanners work as keyboards, so scanning into the box just works.

## Test
`pip install pytest && pytest -q`

## Build a Windows .exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SimplePOS main.py
```
The app is created in `dist/`.
