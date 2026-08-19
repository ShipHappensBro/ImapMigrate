from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from config.settings import settings
from dto.imap_folder import ImapFolder
from dto.worker import Worker
from logger import logger
from services.imap import *
from services.worker import WorkerRunner


def start_migration(
    source_folders: list[ImapFolder],
    workers_count: int,
    runner: WorkerRunner,
    workers: list[Worker],
    source_user: str,
    target_user: str,
):
    """
    Начать миграцию папок между серверами

    Args:
        source_folders (list[ImapFolder]): Список объектов imap папок
        workers_count (int): Количество рабочих
        runner (WorkerRunner): Объект WorkerRunner
        workers (list[Worker]): Список объектов консалидированных рабочих
        source_user (str): email исходного пользователя
        target_user (str): email целевого пользователя
    """
    with (
        tqdm(
            total=len(source_folders),
            desc="Migration",
            unit="folder",
        ) as progress,
        ThreadPoolExecutor(
            max_workers=workers_count,
        ) as executor,
    ):
        futures = [
            executor.submit(
                runner.run,
                worker_data.id,
                folders=worker_data.folders,
                host1=settings.source.server,
                host2=settings.target.server,
                port1=settings.source.port,
                port2=settings.target.port,
                user1=source_user,
                user2=target_user,
                auth_user1=settings.source.auth_user,
                auth_user2=settings.target.auth_user,
                password1=settings.source.password.get_secret_value(),
                password2=settings.target.password.get_secret_value(),
                progress=progress,
            )
            for worker_data in workers
        ]

        for future in futures:
            try:
                future.result()
            except RuntimeError:
                logger.exception(
                    "Ошибка при выполнении worker",
                )
