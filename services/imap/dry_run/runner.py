from loguru import logger
from tqdm import tqdm

from config.settings import settings
from services.imap.commands.command_runner import command_configurate
from services.imap.dry_run.interfaces import IImapSyncDryRun
from services.imap.events import STOP_EVENT


class ImapSyncDryRun(IImapSyncDryRun):
    """Реализация запуска dry-run режима imapsync"""
    def dry_run(
        self,
        host1: str,
        host2: str,
        user1: str,
        user2: str,
        auth_user1: str,
        auth_user2: str,
        password1: str,
        password2: str,
        port1: int = 993,
        port2: int = 993,
    ) -> None:
        """_summary_

        Args:
            host1 (str): Исходный сервер
            host2 (str): Целевой сервер
            user1 (str): Исходный пользователь
            user2 (str): Целевой пользователь
            auth_user1 (str): Исходная имперсонированная учетная запись
            auth_user2 (str): Целевая имперсонированная учетная запись
            password1 (str):  Исходный пароль имперсонированный учетной записи
            password2 (str): Целевой пароль имперсонированный учетной записи
            port1 (int, optional): Исходный порт. Defaults to 993.
            port2 (int, optional): Целевой порт. Defaults to 993.
        """
        if STOP_EVENT.is_set():
            return
        command: tuple[str, ...] = (
            "./imapsync",
            "--dry",
            "--host1",
            host1,
            "--port1",
            str(port1),
            "--authuser1",
            auth_user1,
            "--user1",
            user1,
            "--password1",
            password1,
            "--host2",
            host2,
            "--port2",
            str(port2),
            "--authuser2",
            auth_user2,
            "--user2",
            user2,
            "--password2",
            password2,
            "--nolog",
        )

        logger.info("Начинаем imapsync dry-run")
        name = "Dry"
        process_name = "Default Imapsync Dry-run"
        with tqdm(
            total=1,
            desc="Dry runner",
            unit="run",
        ) as progress:
            command_configurate(
                progress=progress,
                command=command,
                name=name,
                process_name=process_name,
            )


def dry_run(source_user: str, target_user: str):
    ImapSyncDryRun().dry_run(
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
    )
