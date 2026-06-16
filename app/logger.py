import logging
from pathlib import Path

from app.config import get_settings


def setup_logger():

    settings = get_settings()

    Path("logs").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=settings.log_level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(filename)s | "
            "%(funcName)s | "
            "%(message)s"
        ),
    )

    return logging.getLogger("crypto_app")


logger = setup_logger()
