import os
import subprocess
from pathlib import Path
from click.testing import CliRunner

from gitwhodid import __version__
from gitwhodid.cli import main


def test_help_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "usage".title() in result.output


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_gitwhodid_basic(tmp_path: Path) -> None:
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
    subprocess.run(["git"] + list(args), check=True)
