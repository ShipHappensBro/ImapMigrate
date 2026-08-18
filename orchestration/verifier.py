import imaplib

from config.settings import *
from dto.imap_folder import ImapFolder
from services.imap import *
from services.imap.messages.checker import ImapMessageVerifier


def verify(source_folders: list[ImapFolder], target_user: str):
    target_msg_counter = ImapMessageCounter()
    target_authenticator = ImapAuthenticator(AUTH_USER_TARGET, PASSWORD_TARGET)
    target_parser = ImapFolderParser()
    target_provider = ImapFolderProvider(target_parser)
    target_imap = imaplib.IMAP4_SSL(TARGET_SERVER, PORT_TARGET)
    msg_verifer = ImapMessageVerifier()
    msg_verifer.verify(
        source_folders=source_folders,
        target_user=target_user,
        target_imap_message_counter=target_msg_counter,
        target_authenticator=target_authenticator,
        target_provider=target_provider,
        target_imap=target_imap,
    )
