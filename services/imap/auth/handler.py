import imaplib

from services.imap.auth.interfaces import IImapAuthenticator


class ImapAuthenticator(IImapAuthenticator):

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

        def auth_plain(_: bytes) -> bytes:
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