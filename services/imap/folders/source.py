import imaplib

from config.settings import settings
from dto.imap_folder import ImapFolder
from logger import logger
from services.imap import *


def get_source_folders(
    source_imap: imaplib.IMAP4_SSL,
    source_user: str,
) -> list[ImapFolder]:
    """
    Получение папок с исходного сервера

    Args:
        source_imap (imaplib.IMAP4_SSL): Объект imap сервера
        source_user (str): email исходного пользователя

    Returns:
        list[ImapFolder]: Список imap папок
    """
    authenticator = ImapAuthenticator(settings.source.auth_user, settings.source.password.get_secret_value())
    folder_parser = ImapFolderParser()
    folder_provider = ImapFolderProvider(folder_parser)

    message_counter = ImapMessageCounter()

    try:
        logger.info("Подключение к IMAP: {}:{}", settings.source.server, settings.source.port)
        authenticator.authenticate(
            user=source_user,
            imap=source_imap,
        )
        logger.success(
            "Авторизация пользователя {} выполнена",
            source_user,
        )

        source_folders = folder_provider.get(source_imap)
        logger.info(
            "Получено папок: {}",
            len(source_folders),
        )
        for folder in source_folders:
            folder.msg_count = message_counter.get_count(
                imap=source_imap,
                folder=folder,
            )
            logger.debug(
                "Папка: {} [{}] — {} сообщений",
                folder.name,
                folder.imap_name,
                folder.msg_count,
            )

    except Exception:
        logger.exception(
            "Ошибка при получении данных исходного ящика",
        )
        raise

    finally:
        try:
            source_imap.close()
        except Exception:
            logger.exception(
                "Не удалось корректно закрыть IMAP-соединение",
            )
            raise
    return source_folders
