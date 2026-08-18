from loguru import logger
from tqdm import tqdm

from config.settings import *
from services.imap.commands.command_runner import command_configurate
from services.imap.dry_run.interfaces import IImapSyncDryRun
from services.imap.events import STOP_EVENT


class ImapSyncDryRun(IImapSyncDryRun):
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


def dry_run(current_user: str, target_user: str):
    ImapSyncDryRun().dry_run(
        host1=SOURCE_SERVER,
        host2=TARGET_SERVER,
        port1=PORT_SOURCE,
        port2=PORT_TARGET,
        user1=current_user,
        user2=target_user,
        auth_user1=AUTH_USER_SOURCE,
        auth_user2=AUTH_USER_TARGET,
        password1=PASSWORD_SOURCE,
        password2=PASSWORD_TARGET,
    )
