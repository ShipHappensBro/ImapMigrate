from dto.imap_folder import ImapFolder
from logger import logger
from services.imap.folders.runner import ImapSyncFolderRunner
from services.worker.interfaces import IWorkerRunner


class WorkerRunner(IWorkerRunner):
    """
    Класс рабочего для запуска imapsync реализации

    """
    def run(self, id: int, folders: list[ImapFolder], *args, **kwargs) -> None:
        """
        Основная функция запуска миграции папок между серверами

        Args:
            id (int): идентификатор рабочего
            folders (list[ImapFolder]): список папок
        """
        message_count = sum(folder.msg_count for folder in folders)

        logger.info(
            "Worker {} запущен: {} папок, {} сообщений",
            id,
            len(folders),
            message_count,
        )

        try:
            for folder in folders:
                logger.debug(
                    "Worker {}: начинаем миграцию папки {} ({} сообщений)",
                    id,
                    folder.name,
                    folder.msg_count,
                )
                runner = ImapSyncFolderRunner()
                runner.run(
                    folder=folder,
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
