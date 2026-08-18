from typing import Protocol


class IImapSyncDryRun(Protocol):
    """Интерфейс dry-run запуска imapsync"""
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
    ) -> None: ...
