import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "automation.log"


def get_logger(name):
    LOGS_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
