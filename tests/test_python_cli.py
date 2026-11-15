import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PACKS = list(json.loads(Path("packs.json").read_text())["packs"])


def run(*args, check=True):
    return subprocess.run(["fullstack-dev-skill", *args], capture_output=True, text=True, check=check, env={"NO_COLOR": "1", "PATH": str(Path(sys.executable).parent) + ":/usr/bin:/bin"})


def test_version_matches_npm():
    assert run("--version").stdout.strip() == json.loads(Path("package.json").read_text())["version"]


def test_list():
    out = run("list").stdout
    assert all(p in out for p in PACKS)


@pytest.mark.parametrize("pack", PACKS)
def test_install_each_pack(tmp_path, pack):
    run("install", pack, "--dir", str(tmp_path))
    assert (tmp_path / pack / "SKILL.md").read_text().startswith(f"---\nname: {pack}\n")


def test_overwrite_and_uninstall(tmp_path):
    run("install", "fullstack-web", "--dir", str(tmp_path))
    assert run("install", "fullstack-web", "--dir", str(tmp_path), check=False).returncode == 1
    run("install", "fullstack-web", "--dir", str(tmp_path), "--force")
    run("uninstall", "fullstack-web", "--dir", str(tmp_path))
    assert not (tmp_path / "fullstack-web").exists()
    assert run("install", "nope", "--dir", str(tmp_path), check=False).returncode == 1


def test_zip(tmp_path):
    out = tmp_path / "v.zip"
    run("zip", "fullstack-video", "-o", str(out))
    names = zipfile.ZipFile(out).namelist()
    assert "fullstack-video/SKILL.md" in names
    assert any(n.startswith("fullstack-video/templates/remotion-video/") for n in names)
