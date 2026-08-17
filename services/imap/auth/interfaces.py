import imaplib
from typing import Protocol


class IImapAuthenticator(Protocol):
    def authenticate(
        self,
        user: str,
        imap: imaplib.IMAP4_SSL,
    ) -> None: ...
