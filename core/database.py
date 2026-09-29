import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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
    future=True
)

# Фабрика асинхронних сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
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
    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {e}")
        raise e

# Асинхронний генератор сесій із автоматичним закриттям та rollback при помилках
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Транзакцію скасовано через помилку: {e}")
            raise e
        finally:
            await session.close()
            
    