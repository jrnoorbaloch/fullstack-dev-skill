"""Installer for the Full-Stack Developer skill for Claude."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("fullstack-dev-skill")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0"
