import imaplib

from dto.imap_folder import ImapFolder
from services.imap.messages.interfaces import IImapMessageCounter


class ImapMessageCounter(IImapMessageCounter):
    """Класс получения количества сообщений папки с сервера"""
    def get_count(
        self,
        imap: imaplib.IMAP4_SSL,
        folder: ImapFolder,
    ) -> int:
        """
        Получает количество сообщений с imap сервера

        Args:
            imap (imaplib.IMAP4_SSL): Объект imap сервера
            folder (ImapFolder): Imap папка

        Raises:
            RuntimeError: Если сервер вернул ответ отличный от OK
            RuntimeError: Если сервер вернул пустой ответ

        Returns:
            int: _description_
        """
        status, data = imap.select(
            folder.imap_name,
            readonly=True,
        )

        if status != "OK":
            raise RuntimeError(f"Не удалось открыть папку {folder.name}: {data}")

        if not data or data[0] is None:
            raise RuntimeError(
                f"IMAP не вернул количество сообщений "
                f"для папки {folder.name!r}: {data!r}"
            )

        return int(data[0])
