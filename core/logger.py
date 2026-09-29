import logging
import sys
from logging.handlers import RotatingFileHandler

from config.settings import settings

# Створюємо каталог для логів, якщо його ще немає
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

log_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def setup_logger(name: str = "nexus_core") -> logging.Logger:
    """Налаштування централізованого логера."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Якщо обробники вже додані, не дублюємо їх
    if logger.hasHandlers():
        return logger

    # 1. Вивід у консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # 2. Запис у файл із ротацією (макс. 5 МБ, зберігаємо 3 останні файли)
    log_file = settings.LOGS_DIR / "nexus_core.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
