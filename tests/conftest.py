import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Перевірте шлях до Base у вашому проєкті (наприклад, core.database або core.models)
from core.database import Base
from core.models import QuizQuestion, User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Окремий event loop для асинхронних тестів."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_engine():
    """Створює тимчасові таблиці в SQLite memory перед кожним тестом."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine) -> AsyncSession:
    """Фікстура чистої асинхронної сесії для тесту."""
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def sample_user(db_session: AsyncSession) -> User:
    """Фікстура для створення звичайного користувача."""
    user = User(
        telegram_id=123456789,
        username="test_user",
        first_name="Test",
        last_name="User",
        role="user",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def admin_user(db_session: AsyncSession) -> User:
    """Фікстура для створення користувача з роллю адміністратора."""
    user = User(
        telegram_id=987654321,
        username="admin_user",
        first_name="Admin",
        last_name="User",
        role="admin",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def sample_question(db_session: AsyncSession) -> QuizQuestion:
    """Фікстура для створення тестового запитання вікторини."""
    question = QuizQuestion(
        question_text="Яка столиця України?",
        options=["Львів", "Київ", "Одеса", "Харків"],
        correct_answer="Київ",
    )
    db_session.add(question)
    await db_session.commit()
    await db_session.refresh(question)
    return question
