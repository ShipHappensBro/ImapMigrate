from imapclient.imap_utf7 import decode

from dto.imap_folder import ImapFolder
from services.imap.folders.interfaces import IImapFolderParser
from utils.re_pattern import LIST_PATTERN


class ImapFolderParser(IImapFolderParser):
    """Класс парсера полученных сырых папок с сервера"""
    def parse(self, raw_folder: bytes) -> ImapFolder:
        """
        Парсер байто в объект ImapFolder

        Args:
            raw_folder (bytes): Cырые байты полученные от сервера imap

        Raises:
            ValueError: Если не подошел паттерн re

        Returns:
            ImapFolder: Объект ImapFolder
        """
        match = LIST_PATTERN.match(raw_folder)

        if not match:
            raise ValueError(f"Не удалось распарсить IMAP LIST: {raw_folder!r}")

        flags_raw = match.group("flags")
        separator_raw = match.group("separator")
        name_raw = match.group("name")

        flags = tuple(flag.decode("ascii") for flag in flags_raw.split())

        separator = separator_raw.decode("ascii").strip('"')
        name = decode(name_raw)

        return ImapFolder(
            name=name,
            imap_name=name_raw,
            flags=flags,
            separator=separator,
            msg_count=0,
        )
