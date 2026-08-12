from dataclasses import dataclass
from typing import Any


@dataclass()
class ImapFolder:
    name: str
    imap_name: str | Any
    flags: tuple[str, ...]
    separator: str
    msg_count: int

@dataclass
class Worker:
    id: int
    folders: list[ImapFolder]
    msg_count: int = 0