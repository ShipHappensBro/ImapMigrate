import subprocess
import threading

from loguru import logger
from tqdm import tqdm

from config import LOG_DIR
from dto import ImapFolder

_STOP_EVENT = threading.Event()


def run_imapsync(
    folder: ImapFolder,
    host1: str,
    host2: str,
    user1: str,
    user2: str,
    auth_user1: str,
    auth_user2: str,
    password1: str,
    password2: str,
    progress: tqdm,
) -> None:
    if _STOP_EVENT.is_set():
        return

    command = [
        "./imapsync",
        "--host1",
        host1,
        "--authuser1",
        auth_user1,
        "--user1",
        user1,
        "--password1",
        password1,
        "--host2",
        host2,
        "--authuser2",
        auth_user2,
        "--user2",
        user2,
        "--password2",
        password2,
        "--folder",
        folder.imap_name,
        "--nofoldersizes",
        "--nofoldersizesatend",
        "--maxsleep",
        "0",
        "--nolog",
    ]

    safe_name = folder.name.replace("/", "_")
    log_file = LOG_DIR / f"{safe_name}.log"

    logger.info(
        "Начинаем миграцию папки {} ({} сообщений)",
        folder.name,
        folder.msg_count,
    )

    process: subprocess.Popen[bytes] | None = None

    try:
        with log_file.open("w", encoding="utf-8") as log:
            process = subprocess.Popen(
                command,
                cwd="./",
                stdout=log,
                stderr=subprocess.STDOUT,
            )

            returncode = process.wait()

    except KeyboardInterrupt:
        _STOP_EVENT.set()

        if process is None:
            logger.warning(
                "imapsync process не был запущен {}",
                folder.name,
            )
            return

        logger.warning(
            "Останавливаем imapsync: {}",
            folder.name,
        )

        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning(
                "imapsync не завершился за 5 секунд: {}. Отправляем SIGKILL",
                "imapsync не завершился за 5 секунд: {}. Отправляем SIGKILL",
                folder.name,
            )

            process.kill()
            process.wait()

        return

    finally:
        progress.update(1)

    if returncode != 0:
        logger.error(
            "Ошибка миграции {}: exit code {}. Log: {}",
            folder.name,
            returncode,
            log_file,
        )
        return

    logger.success(
        "Миграция завершена: {}",
        folder.name,
    )
