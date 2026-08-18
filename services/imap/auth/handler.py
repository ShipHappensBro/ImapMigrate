import imaplib

from services.imap.auth.interfaces import IImapAuthenticator


class ImapAuthenticator(IImapAuthenticator):

    """Реализация plain аутентификации с использованием имперсонации"""

    def __init__(
        self,
        auth_user: str,
        password: str,
    ) -> None:
        self.auth_user = auth_user
        self.password = password

    def authenticate(
        self,
        user: str,
        imap: imaplib.IMAP4_SSL,
    ) -> None:
        """
        Аутентифицирует пользователя и изменяет состояние объекта imap  

        Args:
            user (str): Учетная запись имперсонации
            imap (imaplib.IMAP4_SSL): Объект imap сервера
        """

        def auth_plain(_: bytes) -> bytes:
            """Plain аутентификация"""
            return (
                user.encode()
                + b"\0"
                + self.auth_user.encode()
                + b"\0"
                + self.password.encode()
            )

        status, _ = imap.authenticate(
            "PLAIN",
            auth_plain,
        )

        if status != "OK":
            raise RuntimeError(
                f"IMAP authentication failed for {user}"
            )