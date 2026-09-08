import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings
from core.logger import logger

# Конвертуємо URL бази даних для асинхронного драйвера aiosqlite, якщо це sqlite
db_url = settings.DB_URL
if "./data/" in db_url or "/data/" in db_url:
    os.makedirs(settings.DATA_DIR, exist_ok=True)
if db_url.startswith("sqlite:///"):
    db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")

# Створюємо асинхронний рушій бази даних
engine = create_async_engine(
    db_url,
    echo=False,  # Встановіть True, якщо потрібен детальний SQL-лог у консолі
    future=True
)

# Фабрика асинхронних сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовий клас для всіх моделей БД
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
    