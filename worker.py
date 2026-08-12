from dto import ImapFolder, Worker
from imapsync_process import run_imapsync
from logger import logger


def distribute_folders(
    folders: list[ImapFolder],
    workers_count: int,
) -> list[Worker]:
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


def worker(
    worker_id: int,
    folders: list[ImapFolder],
    *args,
    **kwargs,
) -> None:
    message_count = sum(
        folder.msg_count
        for folder in folders
    )

    logger.info(
        "Worker {} запущен: {} папок, {} сообщений",
        worker_id,
        len(folders),
        message_count,
    )

    try:
        for folder in folders:
            logger.debug(
                "Worker {}: начинаем миграцию папки {} "
                "({} сообщений)",
                worker_id,
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
            worker_id,
        )
        raise

    logger.success(
        "Worker {} завершён: {} папок",
        worker_id,
        len(folders),
    )