
from loguru import logger
from tqdm import tqdm


class TqdmHandler:
    def write(self, message: str) -> None:
        message = message.rstrip()

        if message:
            tqdm.write(message)

    def flush(self) -> None:
        pass


logger.remove()

logger.add(
    TqdmHandler(),
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    colorize=True
)