import imaplib
from typing import Protocol


class IImapAuthenticator(Protocol):
    """Интерфейс класс ответсвенного за аутентификацию"""
    def authenticate(
        self,
        user: str,
        imap: imaplib.IMAP4_SSL,
    ) -> None: ...
