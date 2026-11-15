# Desktop software, CLIs, scripts

## Choose
- Modern cross-platform app with web UI, small installer → **Tauri 2** (React/Vite front-end + Rust core).
- Heavy Node ecosystem needs → **Electron** + electron-builder.
- Python tools / data apps → **PySide6** (Qt) or Tkinter for very simple; package with PyInstaller.
- Windows-only business software on request → C# + WPF/WinUI/.NET MAUI.
- CLI → Python (Typer + Rich) or Node (commander + chalk). Go/Rust for single-binary tools.

## Tauri scaffold
```
npm create tauri-app@latest
npm run tauri dev
npm run tauri build   # creates .msi/.exe, .dmg, .AppImage/.deb
```
- Local DB: SQLite (tauri-plugin-sql) ; settings in app data dir.
- Use Tauri commands for file system / OS access; keep permissions minimal.

## Electron
- Main / preload / renderer split; `contextIsolation: true`, `nodeIntegration: false`; expose a small API via preload.
- Package with electron-builder; auto-update with electron-updater.

## Python desktop / scripts
- `requirements.txt` or `pyproject.toml`, virtualenv, `if __name__ == "__main__":` entry.
- Package: `pyinstaller --onefile --windowed main.py`.
- Logging, argparse/Typer for options, clear error messages.

## Typical desktop features
- Offline-first local DB, import/export (CSV/Excel/PDF), printing/receipts (POS), backup/restore, user roles, auto-update, license key check when asked.
