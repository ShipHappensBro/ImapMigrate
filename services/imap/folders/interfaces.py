import imaplib
from abc import ABC, abstractmethod

from dto import ImapFolder


class IImapFolderProvider(ABC):

    @abstractmethod
    def get(
        self,
        imap: imaplib.IMAP4_SSL,
    ) -> list[ImapFolder]:
        ...

class IImapFolderParser(ABC):

    @abstractmethod
    def parse(self, raw_folder: bytes) -> ImapFolder:
        ...