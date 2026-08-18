import argparse


def parse_args() -> argparse.Namespace:
    """
    Парсинг аргументов проекта для работы с CLI

    Returns:
        argparse.Namespace
    """
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

    parser.add_argument(
        "--dry",
        dest="enable_dry",
        action="store_true",
        default=False,
        help="Включить dry-run",
    )

    parser.add_argument(
        "--verify",
        dest="enable_verify",
        action="store_true",
        default=False,
        help="Включить проверку количества сообщений между серверами",
    )

    return parser.parse_args()
