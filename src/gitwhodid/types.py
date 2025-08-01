"""
gitwhodid.types
Types and dataclasses for gitwhodid module.
"""

from dataclasses import dataclass


@dataclass
class BlameLine:
    """Dataclass for parsed blame output."""

    author: str
    author_time: str
    commit: str

    @staticmethod
    def from_dict(data: dict[str, str]) -> "BlameLine":
        """Construct "BlameLine" dataclass from an object."""
        return BlameLine(
            author=data["author"],
            author_time=data["author_time"],
            commit=data["commit"],
        )


@dataclass
class Contributor:
    """Dataclass for contributer details."""

    author: str
    percent: int
    last_seen: str


@dataclass
class NotableCommit:
    """Dataclass for notable commits of each author."""

    author: str
    commit: str


@dataclass
class Result:
    """Dataclass for finale output."""

    file: str
    loc: int
    contributors: list[Contributor]
    notable_commits: list[NotableCommit]
