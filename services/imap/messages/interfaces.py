import imaplib
from abc import ABC, abstractmethod

from dto import ImapFolder


class IImapMessageCounter(ABC):

    @abstractmethod
    def get_count(
        self,
        imap: imaplib.IMAP4_SSL,
        folder: ImapFolder,
    ) -> int:
        ...