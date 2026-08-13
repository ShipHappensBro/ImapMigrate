from dto.imap_folder import ImapFolder
from dto.worker import Worker
from logger import logger
from services.worker.interfaces import IWorkerDistributer


class WorkerDistributer(IWorkerDistributer):
    def distribute(self, folders: list[ImapFolder], workers_count: int) -> list[Worker]:
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
