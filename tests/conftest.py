import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.database import Base
from core.models import QuizQuestion, User

# Використовуємо SQLite в пам'яті для асинхронного тестування
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
def engine():
    """Створює асинхронний движок SQLAlchemy для тестової БД."""
    return create_async_engine(TEST_DATABASE_URL, echo=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database(engine):
    """Створює всі таблиці перед кожним тестом і видаляє їх після завершення."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(engine):
    """Надає асинхронну сесію БД для тестів."""
    TestingSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with TestingSessionLocal() as session:
        yield session


# --- Фікстури даних ---


@pytest_asyncio.fixture
async def sample_user(db_session: AsyncSession):
    """Фікстура для створення звичайного користувача."""
    user = User(
        telegram_id=123456789,
        username="test_user",
        role="user",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession):
    """Фікстура для створення адміністратора."""
    user = User(
        telegram_id=987654321,
        username="admin_user",
        role="admin",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def sample_question(db_session: AsyncSession):
    """Фікстура для створення питання вікторини."""
    question = QuizQuestion(
        question_text="Sample Question?",
        options=["Option A", "Option B", "Option C", "Option D"],
        correct_option=0,
        explanation="Test explanation",
    )
    db_session.add(question)
    await db_session.commit()
    await db_session.refresh(question)
    return question
