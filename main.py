import argparse
import imaplib
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from config import *
from logger import logger
from services.imap import *
from services.worker import WorkerDistributer, WorkerRunner


def main(
    current_user: str,
    target_user: str,
) -> None:
    logger.info(
        "Начинаем миграцию: {} -> {}",
        current_user,
        target_user,
    )
    authenticator = ImapAuthenticator(
        AUTH_USER,
        PASSWORD
    )
    foler_parser = ImapFolderParser()
    folder_provider = ImapFolderProvider(
        foler_parser
    )
    
    message_counter = ImapMessageCounter()

    imap = imaplib.IMAP4_SSL(HOST, PORT)

    try:
        logger.info("Подключение к IMAP: {}:{}", HOST, PORT)
        authenticator.authenticate(
            user=current_user,
            imap=imap,
        )
        logger.success(
            "Авторизация пользователя {} выполнена",
            current_user,
        )

        folders = folder_provider.get(imap)
        logger.info(
            "Получено папок: {}",
            len(folders),
        )
        for folder in folders:
            folder.msg_count = message_counter.get_count(
                imap=imap,
                folder=folder,
            )
            logger.debug(
                "Папка: {} [{}] — {} сообщений",
                folder.name,
                folder.imap_name,
                folder.msg_count,
            )

    except Exception:
        logger.exception(
            "Ошибка при получении данных исходного ящика",
        )
        raise

    finally:
        try:
            imap.close()
        except Exception:
            logger.warning(
                "Не удалось корректно закрыть IMAP-соединение",
            )

    workers_count = min(len(folders), 16)

    logger.info(
        "Запускаем миграцию: {} папок, {} workers",
        len(folders),
        workers_count,
    )

    distributer = WorkerDistributer()

    workers = distributer.distribute(
        folders,
        workers_count=workers_count,
    )

    runner = WorkerRunner()

    with (
        tqdm(
            total=len(folders),
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
                host1=HOST,
                host2=HOST2,
                user1=current_user,
                user2=target_user,
                auth_user1=AUTHUSER1,
                auth_user2=AUTHUSER2,
                password1=PASSWORD1,
                password2=PASSWORD2,
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
    logger.success(
        "Миграция {} -> {} завершена",
        current_user,
        target_user,
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="IMAP mailbox migration",
    )

    parser.add_argument(
        "current_user",
        help="Исходный IMAP пользователь",
    )

    parser.add_argument(
        "target_user",
        help="Целевой IMAP пользователь",
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    main(
        current_user=args.current_user,
        target_user=args.target_user,
    )