from abc import ABC, abstractmethod

from dto.imap_folder import ImapFolder
from dto.worker import Worker


class IWorkerDistributer(ABC):
    def distribute(
        self, folders: list[ImapFolder], workers_count: int
    ) -> list[Worker]: ...


class IWorkerRunner(ABC):
    @abstractmethod
    def run(self, id: int, folders: list[ImapFolder]) -> None: ...
