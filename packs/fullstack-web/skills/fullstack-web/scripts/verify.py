#!/usr/bin/env python3
"""Detect the project type and run its install / lint / test / build steps. Exits non-zero on the first failure.

Usage: python verify.py [project-dir] [--skip-install]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> bool:
    print(f"\n$ {' '.join(cmd)}", flush=True)
    try:
        return subprocess.run(cmd, cwd=cwd).returncode == 0
    except FileNotFoundError:
        print(f"  command not found: {cmd[0]}")
        return False


def node_steps(d: Path, install: bool) -> list[list[str]]:
    pm = "pnpm" if (d / "pnpm-lock.yaml").exists() else "yarn" if (d / "yarn.lock").exists() else "npm"
    scripts = json.loads((d / "package.json").read_text()).get("scripts", {})
    steps = [[pm, "install"]] if install else []
    for name in ("lint", "typecheck", "test", "build"):
        if name in scripts:
            steps.append([pm, "run", name] if pm == "npm" else [pm, name])
    return steps


def python_steps(d: Path, install: bool) -> list[list[str]]:
    py = sys.executable
    steps: list[list[str]] = []
    if install and (d / "requirements.txt").exists():
        steps.append([py, "-m", "pip", "install", "-r", "requirements.txt"])
    files = [str(p.relative_to(d)) for p in d.rglob("*.py") if ".venv" not in p.parts]
    if files:
        steps.append([py, "-m", "py_compile", *files])
    if list(d.rglob("test_*.py")) or (d / "tests").exists():
        steps.append([py, "-m", "pytest", "-q"])
    return steps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default=".")
    ap.add_argument("--skip-install", action="store_true")
    a = ap.parse_args()
    d = Path(a.dir).resolve()
    install = not a.skip_install

    if (d / "package.json").exists():
        kind, steps = "node", node_steps(d, install)
    elif (d / "requirements.txt").exists() or (d / "pyproject.toml").exists() or list(d.glob("*.py")):
        kind, steps = "python", python_steps(d, install)
    elif (d / "Cargo.toml").exists():
        kind, steps = "rust", [["cargo", "build"], ["cargo", "test"]]
    elif (d / "go.mod").exists():
        kind, steps = "go", [["go", "vet", "./..."], ["go", "test", "./..."], ["go", "build", "./..."]]
    elif (d / "pubspec.yaml").exists():
        kind, steps = "flutter", [["flutter", "pub", "get"], ["flutter", "analyze"], ["flutter", "test"]]
    elif (d / "composer.json").exists():
        kind, steps = "php", [["composer", "install"], ["php", "artisan", "test"]] if (d / "artisan").exists() else [["composer", "install"]]
    elif list(d.glob("*.html")):
        kind, steps = "static", []
    else:
        print("Could not detect project type.")
        return 2

    print(f"Detected: {kind} project at {d}")
    for step in steps:
        if not run(step, d):
            print(f"\n✗ FAILED: {' '.join(step)}")
            return 1

    if kind == "static":
        bad = []
        for html in d.glob("*.html"):
            text = html.read_text(encoding="utf-8")
            for tag in ("<title>", 'name="viewport"', "<html lang="):
                if tag not in text:
                    bad.append(f"{html.name}: missing {tag}")
        for b in bad:
            print("  ⚠", b)
    env_ex = d / ".env.example"
    if not env_ex.exists() and kind in ("node", "python"):
        print("  ⚠ No .env.example found (run gen_env_example.py if the app uses env vars).")
    print("\n✓ All checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
