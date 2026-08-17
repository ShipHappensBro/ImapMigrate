import imaplib
from typing import Protocol

from dto.imap_folder import ImapFolder
from services.imap.auth.interfaces import IImapAuthenticator
from services.imap.folders.interfaces import IImapFolderProvider


class IImapMessageCounter(Protocol):
    def get_count(
        self,
        imap: imaplib.IMAP4_SSL,
        folder: ImapFolder,
    ) -> int: ...


class IImapMessagesComparer(Protocol):
    def compare(
        self,
        source_imap: imaplib.IMAP4_SSL,
        targe_imap: imaplib.IMAP4_SSL,
    ) -> bool: ...


class IImapMessageVerifier(Protocol):
    def verify(
        self,
        source_folders: list[ImapFolder],
        target_authenticator: IImapAuthenticator,
        target_provider: IImapFolderProvider,
        target_imap: imaplib.IMAP4_SSL,
    ) -> bool: ...
