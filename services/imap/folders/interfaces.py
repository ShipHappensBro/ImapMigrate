import imaplib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

from tqdm import tqdm

from dto.imap_folder import ImapFolder


class IImapFolderProvider(ABC):
    @abstractmethod
    def get(
        self,
        imap: imaplib.IMAP4_SSL,
    ) -> list[ImapFolder]: ...


class IImapFolderParser(ABC):
    @abstractmethod
    def parse(self, raw_folder: bytes) -> ImapFolder: ...


class IImapSyncFolderRunner(Protocol):
    def run(
        self,
        folder: ImapFolder,
        log_file: Path,
        host1: str,
        host2: str,
        user1: str,
        user2: str,
        auth_user1: str,
        auth_user2: str,
        password1: str,
        password2: str,
        progress: tqdm,
        port1: int = 993,
        port2: int = 993,
    ): ...
