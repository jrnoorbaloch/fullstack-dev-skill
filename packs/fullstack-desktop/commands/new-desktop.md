---
description: Build desktop software (POS, inventory, tools) with an installer
argument-hint: "<software purpose and features, target OS>"
---
Use the fullstack-desktop skill to build this desktop software: $ARGUMENTS

1. Pick the stack from `references/desktop.md` (Python + Tkinter/PySide6 for shop tools, Tauri or Electron for modern UI).
2. For POS / billing / inventory, start from `templates/python-desktop-pos` via `scripts/scaffold.py` and extend it.
3. Keep business logic in a testable module, write pytest tests, run `scripts/verify.py`.
4. Explain how to package it (.exe / .dmg / .AppImage).
