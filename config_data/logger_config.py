import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent


def configure_logger(level: int = logging.INFO) -> None:
    """
    Configure the logger.

    :param level: default logger level
    :type level: int
    """
    logging.basicConfig(
        handlers=[
            TimedRotatingFileHandler(filename=(BASE_DIR / "logs/logs.log"),
                                     when="midnight",
                                     backupCount=5,
                                     encoding="utf-8")
        ],
        level=level,
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H-%M-%S"
    )
