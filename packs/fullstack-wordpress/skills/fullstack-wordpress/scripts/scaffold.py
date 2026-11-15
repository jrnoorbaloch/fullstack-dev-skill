#!/usr/bin/env python3
"""Copy a starter template into a new project folder and fill placeholders.

Usage:
  python scaffold.py --list
  python scaffold.py <template> <target-dir> [--set KEY=VALUE ...]

Example:
  python scaffold.py landing-page ./ali-bakery --set BRAND="Ali Bakery" --set TAGLINE="Fresh every morning"
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
TEXT_EXT = {".html", ".md", ".json", ".ts", ".tsx", ".js", ".mjs", ".css", ".py", ".txt", ".sql", ".toml", ".yml", ".yaml", ".example", ".php", ".scss"}
SKIP = {"node_modules", ".next", ".expo", "__pycache__", ".pytest_cache", ".venv", "dist", "build"}


def list_templates() -> list[str]:
    return sorted(p.name for p in TEMPLATES.iterdir() if p.is_dir())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("template", nargs="?")
    ap.add_argument("target", nargs="?")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="replace {{KEY}} with VALUE")
    ap.add_argument("--list", action="store_true", help="list available templates")
    ap.add_argument("--force", action="store_true", help="allow a non-empty target directory")
    args = ap.parse_args()

    if args.list or not args.template:
        print("Available templates:\n  " + "\n  ".join(list_templates()))
        return 0
    if args.template not in list_templates():
        print(f"Unknown template '{args.template}'. Use --list.", file=sys.stderr)
        return 1
    if not args.target:
        print("Target directory is required.", file=sys.stderr)
        return 1

    target = Path(args.target).resolve()
    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"{target} is not empty (use --force).", file=sys.stderr)
        return 1

    values: dict[str, str] = {}
    for item in args.set:
        if "=" not in item:
            print(f"Bad --set '{item}', expected KEY=VALUE", file=sys.stderr)
            return 1
        k, v = item.split("=", 1)
        values[k.strip()] = v

    shutil.copytree(TEMPLATES / args.template, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*SKIP))

    changed = 0
    for f in target.rglob("*"):
        if f.is_file() and (f.suffix in TEXT_EXT or f.name.startswith(".env")):
            text = f.read_text(encoding="utf-8")
            new = text
            for k, v in values.items():
                new = new.replace("{{" + k + "}}", v)
            if new != text:
                f.write_text(new, encoding="utf-8")
                changed += 1

    leftover = sorted({f.relative_to(target).as_posix() for f in target.rglob("*") if f.is_file() and f.suffix in TEXT_EXT and "{{" in f.read_text(encoding="utf-8")})
    print(f"Created {args.template} at {target} ({changed} files filled).")
    if leftover:
        print("Placeholders still to fill in: " + ", ".join(leftover))
    return 0


if __name__ == "__main__":
    sys.exit(main())
