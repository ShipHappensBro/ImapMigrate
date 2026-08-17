from imaplib import IMAP4_SSL

from dto.imap_folder import ImapFolder
from logger import logger
from services.imap.auth.interfaces import IImapAuthenticator
from services.imap.folders.interfaces import IImapFolderProvider
from services.imap.messages.interfaces import (
    IImapMessageCounter,
    IImapMessagesComparer,
    IImapMessageVerifier,
)


class ImapMessagesComparer(IImapMessagesComparer):
    def compare(self, source_imap: IMAP4_SSL, targe_imap: IMAP4_SSL) -> bool:
        raise NotImplementedError()


class ImapMessageVerifier(IImapMessageVerifier):
    def verify(
        self,
        source_folders: list[ImapFolder],
        target_user: str,
        target_imap_message_counter: IImapMessageCounter,
        target_authenticator: IImapAuthenticator,
        target_provider: IImapFolderProvider,
        target_imap: IMAP4_SSL,
    ) -> bool:

        target_authenticator.authenticate(target_user, target_imap)
        target_folders = target_provider.get(target_imap)

        for target_folder in target_folders:
            target_folder.msg_count = target_imap_message_counter.get_count(
                imap=target_imap,
                folder=target_folder,
            )
            logger.debug(
                "Целевая папка: {} [{}] — {} сообщений",
                target_folder.name,
                target_folder.imap_name,
                target_folder.msg_count,
            )
        target_folders.sort(key=lambda folder: folder.name)
        source_folders.sort(key=lambda folder: folder.name)

        errors: dict[str, int] = {}

        for tf, sf in zip(target_folders, source_folders):
            if tf.msg_count != sf.msg_count:
                logger.warning(
                    "Message count mismatch: source folder={} ({}), target folder={} ({})",
                    sf.name,
                    sf.msg_count,
                    tf.name,
                    tf.msg_count,
                )
                errors[tf.name] = sf.msg_count - tf.msg_count
                continue
            logger.success(
                "Message count matched: source folder={} ({}), target folder={} ({})",
                sf.name,
                sf.msg_count,
                tf.name,
                tf.msg_count,
            )
        return bool(errors)
