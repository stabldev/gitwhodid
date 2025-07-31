from datetime import datetime

from gitwhodid.types import Result


def human_time(t: int):
    dt = datetime.fromtimestamp(t)
    return dt.strftime("%Y-%m-%d %H:%M")

def print_result(result: Result):
    print(f"📄 File: {result.file}")
    print(f"📏 Total lines: {result.loc}\n")

    print("👥 Top contributors:")
    medals = ["🥇", "🥈", "🥉"]
    for i, contributer in enumerate(result.contributors):
        medal = medals[i] if i < 3 else " "
        author = contributer.author
        percent = f"{contributer.percent}%"
        print(f"    {medal} {author} - {percent} (last seen {contributer.last_seen})")

    print("\n💬 Notable commits:")
    for commit in result.notable_commits:
        print(f'    "{commit.commit}" - {commit.author}')
