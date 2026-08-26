"""Regression test: package version metadata stays aligned."""

from pathlib import Path
import subprocess
import sys
import tomllib

import md2html

REPO_ROOT = Path(__file__).resolve().parents[1]


def _pyproject_version() -> str:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    return data["project"]["version"]


def test_package_version_matches_pyproject():
    assert md2html.__version__ == _pyproject_version()


def test_cli_version_matches_package():
    result = subprocess.run(
        [sys.executable, "-m", "md2html.cli", "--version"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    assert md2html.__version__ in result.stdout
