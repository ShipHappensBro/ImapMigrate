import imaplib

from dto.imap_folder import ImapFolder
from services.imap.messages.interfaces import IImapMessageCounter


class ImapMessageCounter(IImapMessageCounter):
    def get_count(
        self,
        imap: imaplib.IMAP4_SSL,
        folder: ImapFolder,
    ) -> int:
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
