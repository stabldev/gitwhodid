"""
gitwhodid.blame
Main class for parsing `git blame` output and returning a structured result.
"""

import subprocess
from collections import Counter, defaultdict

from gitwhodid.types import BlameLine, Contributor, NotableCommit, Result
from gitwhodid.utils import format_time


# pylint: disable=too-few-public-methods
class Blame:
    """Parses `git blame` output and stores the result as BlameLine objects.

    This class provides a `run(file)` method that execute `git blame` on the
    given file and returns a structured result.

    Attributes:
        blames (list[BlameLine]): Parsed blame lines.
    """
    def __init__(self) -> None:
        self.blames: list[BlameLine] = []

    def run(self, file: str) -> Result:
        """Runs `git blame` on the given file and returns a structured result.

        The result includes metadata such as filename, number of lines of code,
        list of contributors, and notable commits.

        Args:
            file (str): Path to the file to analyze.

        Returns:
            Result: A dataclass containing information parsed from the git blame output.

        Raises:
            RuntimeError: If the file is inaccessible, invalid or does not exist.
        """
        try:
            self.blames = self._get_blames(file)
            notable_commits = self._get_notable_commits()
            contributors = self._get_contributors()
            contributors.sort(key=lambda x: x.percent, reverse=True)

            return Result(
                file=file,
                loc=len(self.blames),
                contributors=contributors,
                notable_commits=notable_commits,
            )

        except Exception as e:
            raise RuntimeError(f"an unexpected error occurred: {e}") from e

    @staticmethod
    def _get_blames(file: str) -> list[BlameLine]:
        """Runs `git blame` on the given file and parse its output.

        Loop over the parsed output, line by line and extracts blame metadata
        such as author, time, commit summary from the porceclain-format output
        and returns a list of BlameLine objects.

        Args:
            file (str): Path to the file to parse.

        Returns:
            list[BlameLine]: A list of constructed blame objects.
        """
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
        """Finds each authors most frequent commit from the blame results.

        Loop over the blames and construct a counter object which increments over each iteration
        and returns the most common commit of each author.

        Returns:
            list[NotableCommit]: A list of notable commit objects.
        """
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
        """Calculates contributer percentages and last active time.

        Uses blame data to determine how much each author contributed
        and when they last modified the file.

        Returns:
            list[Contributor]: A list of contributor objects.
        """
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
