from dataclasses import dataclass


@dataclass
class BlameLine:
    author: str
    author_time: str
    commit: str

    @staticmethod
    def from_dict(data: dict[str, str]) -> "BlameLine":
        return BlameLine(
            author=data["author"],
            author_time=data["author_time"],
            commit=data["commit"],
        )


@dataclass
class Contributor:
    author: str
    percent: int
    last_seen: str


@dataclass
class NotableCommit:
    author: str
    commit: str


@dataclass
class Result:
    file: str
    loc: int
    contributors: list[Contributor]
    notable_commits: list[NotableCommit]
