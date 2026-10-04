from collections.abc import Sequence
from datetime import datetime
from typing import Any, Generic, TypeVar

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Select,
    String,
    Text,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

T = TypeVar("T", bound="SoftDeleteMixin")


class ObjectsManager(Generic[T]):
    """Кастомний менеджер за типом Django objects для вибірок у стилі soft delete."""

    def __init__(self, model_cls: type[T]) -> None:
        self.model_cls = model_cls

    def get_base_query(self) -> Select:
        """Повертає базовий запит тільки для активних сутностей."""
        return select(self.model_cls).where(self.model_cls.is_active.is_(True))

    def get_all_with_deleted_query(self) -> Select:
        """Повертає базовий запит для всіх сутностей (включно з видаленими)."""
        return select(self.model_cls)

    async def all(self, session: AsyncSession) -> Sequence[T]:
        """Отримати тільки активні записи."""
        result = await session.execute(self.get_base_query())
        return result.scalars().all()

    async def all_with_deleted(self, session: AsyncSession) -> Sequence[T]:
        """Отримати всі записи включно з soft-deleted."""
        result = await session.execute(self.get_all_with_deleted_query())
        return result.scalars().all()

    async def filter(self, session: AsyncSession, *criteria: Any) -> Sequence[T]:
        """Фільтрація серед активних записів."""
        query = self.get_base_query().where(*criteria)
        result = await session.execute(query)
        return result.scalars().all()


class SoftDeleteMixin:
    """Міксин для реалізації soft delete та кастомного менеджера об'єктів."""

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def delete(self) -> None:
        """Soft delete: позначає сутність як неактивну замість фізичного видалення."""
        self.is_active = False

    async def hard_delete(self, session: AsyncSession) -> None:
        """Фізичне видалення запису з бази даних."""
        await session.delete(self)

    @classmethod
    def all_with_deleted_query(cls) -> Select:
        """Повертає select-запит для всіх сутностей включно з видаленими."""
        return select(cls)

    @classmethod
    async def all_with_deleted(cls, session: AsyncSession) -> Sequence[Any]:
        """Повертає всі сутності включно з soft-deleted."""
        result = await session.execute(select(cls))
        return result.scalars().all()


class User(Base, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # Зв'язок із результатами
    results: Mapped[list["Result"]] = relationship(
        "Result", back_populates="user", cascade="all, delete-orphan"
    )

    objects: ObjectsManager["User"]

    def __repr__(self) -> str:
        return f"<User(telegram_id={self.telegram_id}, role='{self.role}', active={self.is_active})>"


User.objects = ObjectsManager(User)


class QuizQuestion(Base, SoftDeleteMixin):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    question_text: Mapped[Text] = mapped_column(Text, nullable=False)
    options_json: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON-масив відповідей
    correct_option: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    objects: ObjectsManager["QuizQuestion"]

    def __repr__(self) -> str:
        return f"<QuizQuestion(id={self.id}, topic='{self.topic}', active={self.is_active})>"


QuizQuestion.objects = ObjectsManager(QuizQuestion)


class Result(Base, SoftDeleteMixin):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    passed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # Зв'язок із користувачем
    user: Mapped["User"] = relationship("User", back_populates="results")

    objects: ObjectsManager["Result"]

    def __repr__(self) -> str:
        return f"<Result(user_id={self.user_id}, topic='{self.topic}', score={self.score})>"


Result.objects = ObjectsManager(Result)
