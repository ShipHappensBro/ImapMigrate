from dataclasses import dataclass

from dto.imap_folder import ImapFolder


@dataclass
class Worker:
    """DTO-класс, представляющий рабочего для обработки папок imap."""
    id: int
    folders: list[ImapFolder]
    msg_count: int = 0
