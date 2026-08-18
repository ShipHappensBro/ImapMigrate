from dataclasses import dataclass
from typing import Any


@dataclass
class ImapFolder:
    """DTO-класс, представляющий папку IMAP."""
    name: str
    imap_name: str | Any
    flags: tuple[str, ...]
    separator: str
    msg_count: int
