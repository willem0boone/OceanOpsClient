import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / "OceanOpsClient" / "_version.py"
SPEC = importlib.util.spec_from_file_location("OceanOpsClient._version", VERSION_PATH)
assert SPEC and SPEC.loader
_version = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(_version)


def test_get_version_counts_commits_after_01_tag(monkeypatch):
    def fake_check_output(cmd, text=True, **kwargs):
        args = cmd[3:]
        if args == ["describe", "--tags", "--abbrev=0"]:
            return "0.1.0"
        if args == ["rev-list", "0.1.0..HEAD", "--count"]:
            return "3"
        raise AssertionError(f"Unexpected git command: {cmd!r}")

    monkeypatch.setattr(_version.subprocess, "check_output", fake_check_output)

    assert _version.get_version() == "0.1.3"


def test_get_version_counts_commits_after_02_tag(monkeypatch):
    def fake_check_output(cmd, text=True, **kwargs):
        args = cmd[3:]
        if args == ["describe", "--tags", "--abbrev=0"]:
            return "v0.2.0"
        if args == ["rev-list", "v0.2.0..HEAD", "--count"]:
            return "5"
        raise AssertionError(f"Unexpected git command: {cmd!r}")

    monkeypatch.setattr(_version.subprocess, "check_output", fake_check_output)

    assert _version.get_version() == "0.2.5"

