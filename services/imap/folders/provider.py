import imaplib

from dto.imap_folder import ImapFolder
from services.imap.folders.interfaces import (
    IImapFolderParser,
    IImapFolderProvider,
)


class ImapFolderProvider(IImapFolderProvider):
    """Класс выдающий папки с imap пользователя"""

    def __init__(self, parser: IImapFolderParser) -> None:
        self.parser = parser

    def get(
        self,
        imap: imaplib.IMAP4_SSL,
    ) -> list[ImapFolder]:
        """
        Получение готовых к использованию папок imap в виде объекта ImapFolder 

        Args:
            imap (imaplib.IMAP4_SSL): Объект imap сервера

        Raises:
            RuntimeError: Если сервер возвращает ошибку при получении папок.

        Returns:
            list[ImapFolder]: Список Imap папок
        """
        status, folders = imap.list()

        if status != "OK" or folders is None:
            raise RuntimeError(f"Не удалось получить список папок: {status}")

        result: list[ImapFolder] = []

        for raw_folder in folders:
            if not isinstance(raw_folder, bytes):
                continue

            result.append(self.parser.parse(raw_folder))

        return result
