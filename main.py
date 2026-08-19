import imaplib

from config.settings import *
from logger import logger
from orchestration.migration import start_migration
from orchestration.parse_args import parse_args
from orchestration.verifier import verify
from services.imap import *
from services.imap.dry_run.runner import dry_run
from services.imap.folders.source import get_source_folders
from services.worker import WorkerDistributer, WorkerRunner


def main(
    source_user: str, target_user: str, enable_dry: bool,
    enable_verify: bool, workers_count: int
) -> None:
    """
    Головная функция проекта. Точка входа

    Args:
        source_user (str): Исходный email пользователя
        target_user (str): Целевой email пользователя
        enable_dry (bool): Включить dry-run
        enable_verify (bool): Включить проверку колтчества сообщений между серверами
    """
    if enable_dry:
        dry_run(source_user, target_user)

    logger.info(
        "Начинаем миграцию: {} -> {}",
        source_user,
        target_user,
    )
    logger.debug(
        "Количество рабочих: {}",
        workers_count
    )
    source_imap = imaplib.IMAP4_SSL(SOURCE_SERVER, PORT_SOURCE)

    source_folders = get_source_folders(
        source_imap=source_imap, source_user=source_user
    )

    workers_count = min(len(source_folders), workers_count)

    logger.info(
        "Запускаем миграцию: {} папок, {} workers",
        len(source_folders),
        workers_count,
    )

    distributer = WorkerDistributer()

    workers = distributer.distribute(
        source_folders,
        workers_count=workers_count,
    )

    runner = WorkerRunner()

    start_migration(
        source_folders=source_folders,
        workers_count=workers_count,
        runner=runner,
        workers=workers,
        source_user=source_user,
        target_user=target_user,
    )

    if enable_verify and not verify(source_folders, target_user):
        logger.warning(
            "Миграция {} -> {} завершена с ошибками",
            source_user,
            target_user,
        )
        return
    logger.success(
        "Миграция {} -> {} завершена",
        source_user,
        target_user,
    )


if __name__ == "__main__":
    args = parse_args()

    main(
        source_user=args.source_user,
        target_user=args.target_user,
        enable_dry=args.enable_dry,
        enable_verify=args.enable_verify,
        workers_count=args.workers
    )
