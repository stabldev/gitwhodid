"""
tests.test_cli
Test file for CLI commands and logic.
"""

import os
import subprocess
from pathlib import Path

from click.testing import CliRunner

from gitwhodid import __version__
from gitwhodid.cli import main


def test_help_command() -> None:
    """Test if `--help` command is working correctly."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "usage".title() in result.output


def test_version_command() -> None:
    """Test if `--version` command is working correctly."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_gitwhodid_basic(tmp_path: Path) -> None:
    """Test with temporary git repo.

    Initializes a tmp git repo at `tmp_path` / repo directory, create a file and commit by
    a test user. Run the CLI and check if test user exists on the output.

    Args:
        tmp_path: Pytest fixture for working on a temporary directory.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    old_cwd = os.getcwd()
    os.chdir(repo)

    try:
        run_git("init")
        run_git("config", "user.name", "test user")
        run_git("config", "user.email", "test@example.com")

        # create a file and commit it
        file = repo / "test.py"
        file.write_text('print("hello, world!")')
        run_git("branch", "-m", "main")
        run_git("add", "test.py")
        run_git("commit", "-m", "chore: initial commit")

        # run gitwhodid
        runner = CliRunner()
        result = runner.invoke(main, [str(file)], catch_exceptions=False)

        assert result.exit_code == 0
        assert "test user" in result.output
        assert "100%" in result.output
        assert "last seen today" in result.output
        assert "chore: initial commit" in result.output
    finally:
        os.chdir(old_cwd)


def run_git(*args: str) -> None:
    """Runs a git command using subprocess for use in tests.

    Args:
        *args (str): Individual git command arguments (e.g., "init", "status").
    """
    subprocess.run(["git"] + list(args), check=True)
