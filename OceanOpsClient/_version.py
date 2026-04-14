"""Version helpers for OceanOpsClient."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

_DEFAULT_VERSION = "0.1.0"
_VERSION_PATTERN = re.compile(r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")
_REPO_ROOT = Path(__file__).resolve().parents[1]


def _run_git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(_REPO_ROOT), *args],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def _parse_version(tag: str) -> tuple[int, int, int] | None:
    match = _VERSION_PATTERN.match(tag.strip())
    if not match:
        return None
    return tuple(int(match.group(name)) for name in ("major", "minor", "patch"))


def get_version() -> str:
    """Return the package version derived from git metadata.

    The version scheme keeps the release's major/minor line and increments the
    patch number with every commit after the latest release tag. For example:

    - tag ``0.1.0`` -> the next commit becomes ``0.1.1``
    - tag ``0.2.0`` -> the next commit becomes ``0.2.1``
    """

    override = os.getenv("OCEANOPSCLIENT_VERSION", "").strip()
    if override:
        return override

    try:
        latest_tag = _run_git("describe", "--tags", "--abbrev=0")
        major, minor, patch = _parse_version(latest_tag) or (None, None, None)
        if major is None:
            raise ValueError(f"Unsupported release tag: {latest_tag!r}")
        commit_count = int(_run_git("rev-list", f"{latest_tag}..HEAD", "--count"))
        return f"{major}.{minor}.{patch + commit_count}"
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        try:
            commit_count = int(_run_git("rev-list", "HEAD", "--count"))
            base_major, base_minor, base_patch = (int(part) for part in _DEFAULT_VERSION.split("."))
            return f"{base_major}.{base_minor}.{base_patch + commit_count}"
        except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
            return _DEFAULT_VERSION


__version__ = get_version()

