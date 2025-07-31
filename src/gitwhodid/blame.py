from collections import Counter, defaultdict
import subprocess

from gitwhodid.types import BlameLine, Contributor, NotableCommit, Result
from gitwhodid.utils import format_time


class Blame:
    def __init__(self) -> None:
        self.blames: list[BlameLine] = []

    def run(self, file: str) -> Result:
        try:
            self.blames = self._get_blames(file)
            notable_commits = self._get_notable_commits()
            contributors = self._get_contributors()
            # TODO: add flag for sorting
            contributors.sort(key=lambda x: x.percent, reverse=True)

            return Result(
                file=file,
                loc=len(self.blames),
                contributors=contributors,
                notable_commits=notable_commits,
            )

        except Exception as e:
            raise RuntimeError(f"an unexpected error occurred: {e}")

    @staticmethod
    def _get_blames(file: str) -> list[BlameLine]:
        cmd = ["git", "blame", file, "--line-porcelain"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stderr:
            raise RuntimeError(f"standard error: {result.stderr}")

        lines = result.stdout.splitlines()
        blames: list[BlameLine] = []
        current: dict[str, str] = {}

        for line in lines:
            # end of a blame
            if line.startswith("\t"):
                if current:
                    blames.append(BlameLine.from_dict(current))
                    current = {}

            elif line.startswith("author "):
                current["author"] = line[len("author ") :]
            elif line.startswith("author-time "):
                current["author_time"] = line[len("author-time ") :]
            elif line.startswith("summary "):
                current["commit"] = line[len("summary ") :]

        return blames

    def _get_notable_commits(self) -> list[NotableCommit]:
        commit_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
        for blame in self.blames:
            author = blame.author
            commit = blame.commit
            commit_counts[author][commit] += 1

        return [
            NotableCommit(author=author, commit=counts.most_common(1)[0][0])
            for author, counts in commit_counts.items()
        ]

    def _get_contributors(self) -> list[Contributor]:
        last_seen: defaultdict[str, int] = defaultdict(int)
        for blame in self.blames:
            author = blame.author
            time = int(blame.author_time)
            last_seen[author] = max(last_seen[author], time)

        authors_count = Counter(blame.author for blame in self.blames)
        contributers: list[Contributor] = []

        for author, count in authors_count.items():
            percent = (count / len(self.blames)) * 100

            contributers.append(
                Contributor(
                    author=author,
                    percent=round(percent),
                    last_seen=format_time(last_seen[author]),
                )
            )

        return contributers
