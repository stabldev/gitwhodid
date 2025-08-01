"""
gitwhodid.utils
Utility functions for gitwhodid modules.
"""

from datetime import datetime

from rich.console import Console
from rich.table import Table

from gitwhodid.types import Result

console = Console()


def format_time(t: float) -> str:
    """Format a timestamp in a readable format.

    Converts a timestamp (float) time object to a proper string format which is much readable
    and return format is based-on day format..

    Args:
        t (float): A date timestamp object to convert.

    Returns:
        str: Formatted string from the timestamp.
    """
    dt = datetime.fromtimestamp(t)
    delta = datetime.now() - dt
    days = delta.days

    if days == 0:
        return "today"
    if days == 1:
        return "yesterday"
    return f"{days} days ago"


def print_result(result: Result):
    """Prints the result from the `Result` object.

    Uses rich library's `Console` object to print en-riched result such as filename, loc,
    contributors and notable commits of each author.

    Args:
        result (Result): A result object created from the `Blame.run(file)` method.
    """

    console.print(f"[bold magenta]📄 File:[/bold magenta] {result.file}")
    console.print(f"[bold cyan]📏 Total lines:[/bold cyan] {result.loc}\n")

    # contributors
    console.print("[bold green]👥 Top contributors:[/bold green]")
    table = Table(box=None, show_header=False, padding=(0, 1))
    medals = ["🥇", "🥈", "🥉"]
    for i, contributor in enumerate(result.contributors):
        medal = medals[i] if i < 3 else "  "
        last_seen = contributor.last_seen
        table.add_row(
            medal,
            f"[bold]{contributor.author}[/bold]",
            f"{contributor.percent}%",
            f"[dim]last seen {last_seen}[/dim]",
        )
    console.print(table)

    # notable commits
    console.print("\n[bold yellow]💬 Notable commits:[/bold yellow]")
    for commit in result.notable_commits:
        console.print(
            f" • “[italic]{commit.commit}[/italic]” - [bold]{commit.author}[/bold]"
        )
