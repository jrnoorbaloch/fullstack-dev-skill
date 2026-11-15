"""Command-line installer: list / install / uninstall / zip. Mirrors the npm CLI."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

from . import __version__

FULL = "fullstack-developer"
SKIP = {"node_modules", "__pycache__", ".pytest_cache", "dist", "build", "out", ".next", ".expo"}


def data_root() -> Path:
    """Packaged data (wheel) or the repository root (source checkout)."""
    here = Path(__file__).resolve().parent
    if (here / "data" / "packs.json").exists():
        return here / "data"
    repo = here.parent.parent
    if (repo / "packs.json").exists():
        return repo
    raise SystemExit("Error: skill data not found; reinstall the package.")


ROOT = data_root()
CONFIG = json.loads((ROOT / "packs.json").read_text(encoding="utf-8"))


def color(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() and not os.environ.get("NO_COLOR") else s


def fail(msg: str) -> None:
    print(color("31", "Error: ") + msg, file=sys.stderr)
    raise SystemExit(1)


def skill_dir(name: str) -> Path:
    if name not in CONFIG["packs"]:
        fail(f'Unknown pack "{name}". Run "fullstack-dev-skill list" to see available packs.')
    if name == FULL:
        d = ROOT / "skills" / FULL if (ROOT / "skills" / FULL).exists() else ROOT / CONFIG["source"]
    else:
        d = ROOT / "packs" / name / "skills" / name
    if not (d / "SKILL.md").exists():
        fail(f"Pack files not found at {d}")
    return d


def target_base(a: argparse.Namespace) -> Path:
    if a.dir:
        return Path(a.dir).expanduser().resolve()
    if a.project:
        return Path.cwd() / ".claude" / "skills"
    return Path.home() / ".claude" / "skills"


def files_of(src: Path) -> list[Path]:
    out = []
    for p in sorted(src.rglob("*")):
        if p.is_file() and not any(part in SKIP for part in p.relative_to(src).parts):
            out.append(p)
    return out


def cmd_list(_: argparse.Namespace) -> int:
    print(color("1", "Available packs") + f"  (v{__version__})\n")
    for name, p in CONFIG["packs"].items():
        tag = color("32", " (default, everything)") if name == FULL else ""
        print(f"  {color('1', name.ljust(22))} {p['title']}{tag}")
    print('\nInstall one with: fullstack-dev-skill install <pack>')
    return 0


def cmd_install(a: argparse.Namespace) -> int:
    src = skill_dir(a.pack)
    dest = target_base(a) / a.pack
    if dest.exists():
        if not a.force:
            fail(f"{dest} already exists. Use --force to replace it.")
        shutil.rmtree(dest)
    for f in files_of(src):
        t = dest / f.relative_to(src)
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, t)
    print(f"{color('32', '✓')} Installed {color('1', a.pack)} → {dest}")
    print("  Restart Claude Code (or start a new session) to load it. Then just describe what to build.")
    return 0


def cmd_uninstall(a: argparse.Namespace) -> int:
    if a.pack not in CONFIG["packs"]:
        fail(f'Unknown pack "{a.pack}".')
    dest = target_base(a) / a.pack
    if not (dest / "SKILL.md").exists():
        fail(f"{a.pack} is not installed at {dest}")
    shutil.rmtree(dest)
    print(f"{color('32', '✓')} Removed {dest}")
    return 0


def cmd_zip(a: argparse.Namespace) -> int:
    src = skill_dir(a.pack)
    out = Path(a.output or f"{a.pack}.zip").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    files = files_of(src)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f"{a.pack}/{f.relative_to(src).as_posix()}")
    print(f"{color('32', '✓')} Wrote {out} ({len(files)} files)")
    print("  Claude app → Settings → Capabilities → Skills → Upload skill")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fullstack-dev-skill", description="Full-Stack Developer skill for Claude — installer.")
    p.add_argument("-v", "--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list", help="show available packs").set_defaults(func=cmd_list)
    for name, func, helptext in (("install", cmd_install, "install into Claude Code"), ("uninstall", cmd_uninstall, "remove an installed pack")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("pack", nargs="?", default=FULL)
        s.add_argument("--project", action="store_true", help="use ./.claude/skills instead of ~/.claude/skills")
        s.add_argument("--dir", help="custom skills directory")
        if name == "install":
            s.add_argument("--force", "-f", action="store_true", help="replace an existing installation")
        s.set_defaults(func=func, force=False)
    z = sub.add_parser("zip", help="build a zip for the Claude app")
    z.add_argument("pack", nargs="?", default=FULL)
    z.add_argument("-o", "--output", help="output path (default: <pack>.zip)")
    z.set_defaults(func=cmd_zip)

    a = p.parse_args(argv)
    if not getattr(a, "func", None):
        p.print_help()
        return 0
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())
