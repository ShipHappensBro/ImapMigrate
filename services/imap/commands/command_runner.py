import subprocess
from pathlib import Path
from typing import Protocol

from loguru import logger
from tqdm import tqdm

from config.settings import LOG_DIR
from services.imap.commands.exceptions import ImapSyncFinishedWithNonZeroCode
from services.imap.events import STOP_EVENT


class Runner(Protocol):
    """Интерфейс раннера ответственного за создание сессии imapsync"""
    def __call__(
        self,
        log_file: Path,
        name: str,
        process_name: str,
        command: tuple[str, ...],
        progress: tqdm,
    ) -> None: ...


def default_runner(
    log_file: Path,
    name: str,
    process_name: str,
    command: tuple[str, ...],
    progress: tqdm,
):
    """
    Раннер по умолчанию

    Args:
        log_file (Path): путь к лог файлу
        name (str): Название модуля
        process_name (str): Название процесса
        command (tuple[str, ...]): Кортеж команд для imapsync
        progress (tqdm): Tqdm объект для отслеживания процесса

    Raises:
        ImapSyncFinishedWithNonZeroCode: Если imapsync вышел с ненулевым статусом
    """
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
        STOP_EVENT.set()

        if process is None:
            logger.warning(
                "imapsync {}: {} not initialized",
                name,
            )
            return

        logger.warning(
            "[STOPPING] Останавливаем imapsync: {}",
            name,
        )

        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning(
                "{} | imapsync не завершился за 5 секунд: {}. Отправляем SIGKILL",
                process_name,
                name,
            )

            process.kill()
            process.wait()

        return

    finally:
        progress.update(1)

    if returncode != 0:
        raise ImapSyncFinishedWithNonZeroCode(
            code=returncode,
            process_name=process_name,
            name=name,
            log_file=log_file,
        )

    logger.success(
        "{} | Завершено для: {}",
        process_name,
        name,
    )


def command_configurate(
    progress: tqdm,
    runner: Runner = default_runner,
    name: str = "Sended",
    process_name: str = "Migration",
    command: tuple[str, ...] = ("./imapsync", "--dry"),
    *args,
    **kwargs,
):
    """
    Отвечает за формирование раннера

    Args:
        progress (tqdm): Tqdm объект для отслеживания процесса
        runner (Runner, optional): Объект раннера. Defaults to default_runner.
        name (str, optional): Название модуля. Defaults to "migration".
    """
    safe_name = name.replace("/", "_")
    log_file = LOG_DIR / f"{safe_name}.log"
    try:
        runner(
            name=name,
            process_name=process_name,
            log_file=log_file,
            command=command,
            progress=progress,
        )
    except Exception:
        logger.exception("Runner failed")
        raise
