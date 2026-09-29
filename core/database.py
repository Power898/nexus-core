import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings
from core.logger import logger

# Гарантуємо існування директорії для бази даних
if hasattr(settings, "DATA_DIR") and settings.DATA_DIR:
    os.makedirs(settings.DATA_DIR, exist_ok=True)

# Конвертуємо URL бази даних для асинхронного драйвера aiosqlite
db_url = settings.DB_URL
if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite+aiosqlite:///"):
    db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")

# Створюємо асинхронний рушій бази даних
engine = create_async_engine(
    db_url,
    echo=False,  # Встановіть True, якщо потрібен детальний SQL-лог для відлагодження
    future=True,
)

# Фабрика асинхронних сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Базовий клас для всіх ORM-моделей БД
class Base(DeclarativeBase):
    pass


# Функція для ініціалізації БД (створення всіх таблиць)
async def init_db() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Базу даних успішно ініціалізовано.")
    except Exception:
        logger.exception("Помилка при ініціалізації бази даних")
        raise


# Асинхронний генератор сесій із автоматичним закриттям та rollback при помилках
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception("Транзакцію скасовано через помилку")
            raise
        finally:
            await session.close()
