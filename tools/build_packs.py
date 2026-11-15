#!/usr/bin/env python3
"""Build focused skill packs from the complete skill.

The complete skill in skills/fullstack-developer is the single source of truth.
This script copies the subset of references/templates/scripts listed in packs.json
into packs/<pack>/ (a Claude Code plugin containing one skill), rewrites SKILL.md so it
only routes to files that the pack contains, and optionally writes upload-ready zips.

Usage:
  python tools/build_packs.py            # regenerate packs/
  python tools/build_packs.py --check    # fail if packs/ is out of date (CI)
  python tools/build_packs.py --zips dist/zips   # also write <pack>.zip for every pack (incl. the complete skill)
"""
from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "packs.json").read_text(encoding="utf-8"))
SOURCE = ROOT / CONFIG["source"]
FULL = "fullstack-developer"
IGNORE = shutil.ignore_patterns("node_modules", "dist", "build", "out", "__pycache__", ".pytest_cache", ".next", ".expo", "*.pyc")
TOKEN = re.compile(r"`([^`]+)`")
ALL_TEMPLATES = sorted(p.name for p in (SOURCE / "templates").iterdir() if p.is_dir())
ALL_REFERENCES = sorted(p.name for p in (SOURCE / "references").glob("*.md"))
ALL_COMMANDS = sorted(p.stem for p in (ROOT / "commands").glob("*.md"))


def resolve(pack: dict) -> tuple[list[str], list[str], list[str]]:
    core = CONFIG["core"]
    refs = ALL_REFERENCES if pack["references"] == "*" else sorted(set(core["references"]) | set(pack["references"]))
    temps = ALL_TEMPLATES if pack["templates"] == "*" else sorted(pack["templates"])
    cmds = ALL_COMMANDS if pack["commands"] == "*" else sorted(pack["commands"])
    for r in refs:
        assert (SOURCE / "references" / r).exists(), f"missing reference {r}"
    for t in temps:
        assert (SOURCE / "templates" / t).is_dir(), f"missing template {t}"
    for c in cmds:
        assert (ROOT / "commands" / f"{c}.md").exists(), f"missing command {c}"
    return refs, temps, cmds


def missing_target(token: str, refs: set[str], temps: set[str]) -> bool:
    """True if a backticked token points at a reference/template the pack does not contain."""
    if token.startswith("references/"):
        return token.split("/", 1)[1] not in refs
    if token.startswith("templates/"):
        return token.split("/")[1] not in temps
    if token in ALL_TEMPLATES:
        return token not in temps
    m = re.match(r"scaffold\.py (\S+)", token)
    if m and m.group(1) in ALL_TEMPLATES:
        return m.group(1) not in temps
    return False


def pack_skill_md(name: str, pack: dict, refs: list[str], temps: list[str]) -> str:
    text = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
    fm_end = text.index("\n---\n", 4) + 5
    body = text[fm_end:]
    refs_s, temps_s = set(refs), set(temps)

    kept = []
    for line in body.splitlines():
        tokens = TOKEN.findall(line)
        if any(missing_target(t, refs_s, temps_s) for t in tokens):
            continue  # drop table rows / bullets that route to files this pack does not ship
        kept.append(line)
    body = "\n".join(kept) + "\n"

    title = pack["title"]
    body = body.replace(
        "# Full-Stack Developer\n",
        f"# Full-Stack Developer — {title} pack\n\n"
        f"> Focused pack. It contains only the guides and templates for **{title}**. "
        f"For every product type (web, mobile, desktop, animation & 3D, WordPress, video) install the complete "
        f"`fullstack-developer` skill instead.\n",
        1,
    )
    desc = pack["description"]
    assert desc and len(desc) <= 1024, f"{name}: description must be 1-1024 chars"
    return f"---\nname: {name}\ndescription: {desc}\n---\n{body}"


def write_pack(name: str, pack: dict, out: Path) -> None:
    refs, temps, cmds = resolve(pack)
    skill = out / "skills" / name
    (skill / "references").mkdir(parents=True)
    for r in refs:
        shutil.copy2(SOURCE / "references" / r, skill / "references" / r)
    for t in temps:
        shutil.copytree(SOURCE / "templates" / t, skill / "templates" / t, ignore=IGNORE)
    shutil.copytree(SOURCE / "scripts", skill / "scripts", ignore=IGNORE)
    (skill / "SKILL.md").write_text(pack_skill_md(name, pack, refs, temps), encoding="utf-8")

    (out / "commands").mkdir()
    for c in cmds:
        text = (ROOT / "commands" / f"{c}.md").read_text(encoding="utf-8")
        (out / "commands" / f"{c}.md").write_text(text.replace("the fullstack-developer skill", f"the {name} skill"), encoding="utf-8")

    root_plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    plugin = {
        "name": name,
        "description": f"{pack['title']} pack of the Full-Stack Developer skill. " + pack["description"].split(" Use when")[0],
        "version": root_plugin["version"],
        "author": root_plugin["author"],
        "license": root_plugin.get("license", "MIT"),
        "homepage": "https://github.com/jrnoorbaloch/fullstack-dev-skill",
    }
    (out / ".claude-plugin").mkdir()
    (out / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin, indent=2) + "\n", encoding="utf-8")

    readme = [
        f"# {pack['title']} — Full-Stack Developer skill pack",
        "",
        "> Generated by `tools/build_packs.py` from `skills/fullstack-developer`. Do not edit here — edit the complete skill and rebuild.",
        "",
        pack["description"],
        "",
        "## Contents",
        f"- **Guides:** {', '.join(r[:-3] for r in refs)}",
        f"- **Templates:** {', '.join(temps)}",
        f"- **Commands:** {', '.join('/' + c for c in cmds)}",
        "",
        "## Install",
        "```bash",
        f"npx github:jrnoorbaloch/fullstack-dev-skill install {name}",
        f"# or: pip install fullstack-dev-skill && fullstack-dev-skill install {name}",
        f"# or (Claude Code): /plugin install {name}@fullstack-dev-skill",
        "```",
        f"Claude app: download `{name}.zip` from the latest release → Settings → Capabilities → Skills → Upload skill.",
        "",
    ]
    (out / "README.md").write_text("\n".join(readme), encoding="utf-8")


def validate_skill(skill_dir: Path) -> None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", text, re.S)
    assert m, f"{skill_dir}: bad frontmatter"
    assert m.group(1) == skill_dir.name, f"{skill_dir}: name must match folder"
    assert len(m.group(2)) <= 1024
    for tok in set(re.findall(r"`((?:references|templates|scripts)/[\w./-]+)`", text)):
        assert (skill_dir / tok).exists(), f"{skill_dir.name}: SKILL.md points to missing {tok}"


def build(dest: Path) -> list[str]:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    names = []
    for name, pack in CONFIG["packs"].items():
        if name == FULL:
            continue
        write_pack(name, pack, dest / name)
        validate_skill(dest / name / "skills" / name)
        names.append(name)
    return names


def zip_skill(skill_dir: Path, out_zip: Path) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill_dir.rglob("*")):
            rel = f.relative_to(skill_dir.parent)
            if any(part in {"node_modules", "__pycache__", "dist", "build", "out"} for part in rel.parts):
                continue
            if f.is_file():
                z.write(f, rel.as_posix())


def same_tree(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        print("differs:", a, cmp.left_only, cmp.right_only, cmp.diff_files)
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    if mismatch or errors:
        print("differs:", a, mismatch, errors)
        return False
    return all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify packs/ is up to date")
    ap.add_argument("--zips", metavar="DIR", help="also write <pack>.zip files to DIR")
    a = ap.parse_args()

    validate_skill(SOURCE)
    if a.check:
        with tempfile.TemporaryDirectory() as tmp:
            build(Path(tmp) / "packs")
            if not (ROOT / "packs").exists() or not same_tree(Path(tmp) / "packs", ROOT / "packs"):
                print("packs/ is out of date. Run: python tools/build_packs.py")
                return 1
        print("packs/ is up to date")
        return 0

    names = build(ROOT / "packs")
    print(f"Built {len(names)} packs: {', '.join(names)}")
    if a.zips:
        zdir = Path(a.zips)
        zip_skill(SOURCE, zdir / f"{FULL}.zip")
        for n in names:
            zip_skill(ROOT / "packs" / n / "skills" / n, zdir / f"{n}.zip")
        print(f"Zips written to {zdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
