from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from config.settings import *
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
                host1=SOURCE_SERVER,
                host2=TARGET_SERVER,
                port1=PORT_SOURCE,
                port2=PORT_TARGET,
                user1=source_user,
                user2=target_user,
                auth_user1=AUTH_USER_SOURCE,
                auth_user2=AUTH_USER_TARGET,
                password1=PASSWORD_SOURCE,
                password2=PASSWORD_TARGET,
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
