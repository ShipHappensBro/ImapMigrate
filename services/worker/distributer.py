from dto.imap_folder import ImapFolder
from dto.worker import Worker
from logger import logger
from services.worker.interfaces import IWorkerDistributer


class WorkerDistributer(IWorkerDistributer):
    """Реализация распределения папок по рабочим"""
    def distribute(self, folders: list[ImapFolder], workers_count: int) -> list[Worker]:
        """
        Распределяет папки по рабочим в ~равном количестве

        Args:
            folders (list[ImapFolder]): Список imap папок
            workers_count (int): Количество папок

        Returns:
            list[Worker]: Список рабочих
        """
        workers = [
            Worker(
                id=i + 1,
                folders=[],
            )
            for i in range(workers_count)
        ]

        for folder in sorted(
            folders,
            key=lambda folder: folder.msg_count,
            reverse=True,
        ):
            worker = min(
                workers,
                key=lambda worker: worker.msg_count,
            )

            worker.folders.append(folder)
            worker.msg_count += folder.msg_count

        logger.info(
            "Распределено {} папок между {} workers",
            len(folders),
            workers_count,
        )

        for worker in workers:
            if not worker.folders:
                continue

            logger.debug(
                "Worker {}: {} папок, {} сообщений",
                worker.id,
                len(worker.folders),
                worker.msg_count,
            )

        return workers
