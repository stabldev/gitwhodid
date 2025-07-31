from datetime import datetime
from rich.console import Console
from rich.table import Table

from gitwhodid.types import Result

console = Console()


def format_time(t: float) -> str:
    dt = datetime.fromtimestamp(t)
    delta = datetime.now() - dt
    days = delta.days

    if days == 0:
        return "today"
    elif days == 1:
        return "yesterday"
    return f"{days} days ago"


def print_result(result: Result):
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
