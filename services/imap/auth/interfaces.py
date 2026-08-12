import imaplib
from abc import ABC, abstractmethod


class IImapAuthenticator(ABC):

    @abstractmethod
    def authenticate(
        self,
        user: str,
        imap: imaplib.IMAP4_SSL,
    ) -> None:
        ...