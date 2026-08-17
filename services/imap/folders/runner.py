from tqdm import tqdm

from dto.imap_folder import ImapFolder
from services.imap.commands.command_runner import command_configurate
from services.imap.folders.interfaces import IImapSyncFolderRunner


class ImapSyncFolderRunner(IImapSyncFolderRunner):
    def run(
        self,
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
        port1: int = 993,
        port2: int = 993,
    ):
        command = (
            "./imapsync",
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
            "--folder",
            folder.imap_name,
            "--nofoldersizes",
            "--nofoldersizesatend",
            "--maxsleep",
            "0",
            "--nolog",
        )
        process_name = "Миграция"
        command_configurate(
            name=folder.name,
            process_name=process_name,
            command=command,
            progress=progress,
        )
