from pathlib import Path


class ImapSyncFinishedWithNonZeroCode(Exception):
    def __init__(
        self,
        code: int,
        process_name: str,
        name: str,
        log_file: Path,
    ) -> None:
        self.code = code
        self.process_name = process_name
        self.name = name
        self.log_file = log_file

        super().__init__(
            f"{process_name} | Ошибка {name}: exit code {code}. Log: {log_file}"
        )
