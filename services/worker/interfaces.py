from abc import ABC, abstractmethod

from dto.imap_folder import ImapFolder
from dto.worker import Worker


class IWorkerDistributer(ABC):
    """Абстрактный интерфейс для распеределения папок по рабочим"""
    def distribute(
        self, folders: list[ImapFolder], workers_count: int
    ) -> list[Worker]: ...


class IWorkerRunner(ABC):
    """Абстрактный интерфейс для запуска миграций."""
    @abstractmethod
    def run(self, id: int, folders: list[ImapFolder]) -> None: ...
