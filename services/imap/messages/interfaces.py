import imaplib
from typing import Protocol

from dto.imap_folder import ImapFolder
from services.imap.auth.interfaces import IImapAuthenticator
from services.imap.folders.interfaces import IImapFolderProvider


class IImapMessageCounter(Protocol):
    """Интерфейс получения количества сообщений из папки с сервера imap"""

    def get_count(
        self,
        imap: imaplib.IMAP4_SSL,
        folder: ImapFolder,
    ) -> int: ...


class IImapMessagesComparer(Protocol):
    """Интерфейс для сравнения количества сообщений между папок серверов imap"""

    def compare(
        self,
        source_imap: imaplib.IMAP4_SSL,
        targe_imap: imaplib.IMAP4_SSL,
    ) -> bool: ...


class IImapMessageVerifier(Protocol):
    """Интерфейс для проверки количества сообщений между папками IMAP-серверов.
    Используется после миграции.
    """

    def verify(
        self,
        source_folders: list[ImapFolder],
        target_user: str,
        target_imap_message_counter: IImapMessageCounter,
        target_authenticator: IImapAuthenticator,
        target_provider: IImapFolderProvider,
        target_imap: imaplib.IMAP4_SSL,
    ) -> bool: ...
