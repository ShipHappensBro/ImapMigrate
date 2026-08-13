from dto import ImapFolder
from logger import logger
from services.imap.runner import run_imapsync
from services.worker.interfaces import IWorkerRunner


class WorkerRunner(IWorkerRunner):

    def run(
        self, id: int, folders: list[ImapFolder],
        *args, **kwargs
    ) -> None:
        message_count = sum(
            folder.msg_count
            for folder in folders
        )

        logger.info(
            "Worker {} запущен: {} папок, {} сообщений",
            id,
            len(folders),
            message_count,
        )

        try:
            for folder in folders:
                logger.debug(
                    "Worker {}: начинаем миграцию папки {} "
                    "({} сообщений)",
                    id,
                    folder.name,
                    folder.msg_count,
                )

                run_imapsync(
                    folder,
                    **kwargs,
                )

        except Exception:
            logger.exception(
                "Worker {} завершился с ошибкой",
                id,
            )
            raise

        logger.success(
            "Worker {} завершён: {} папок",
            id,
            len(folders),
        )
