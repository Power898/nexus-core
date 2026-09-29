import os
from pathlib import Path

from dotenv import load_dotenv

# Визначаємо базову директорію проєкту (корінь)
BASE_DIR = Path(__file__).resolve().parent.parent

# Завантажуємо змінні з файлу .env
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Централізований клас конфігурації проєкту."""

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", os.getenv("TELEGRAM_BOT_TOKEN", ""))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-dev-key")
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./data/nexus.db")

    # Шляхи до системних каталогів
    LOGS_DIR: Path = BASE_DIR / "logs"
    DATA_DIR: Path = BASE_DIR / "data"

    @classmethod
    def validate(cls) -> None:
        """Перевірка наявності критичних змінних."""
        if cls.ENVIRONMENT == "production" and not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN обов'язковий для production середовища!")


settings = Settings()
