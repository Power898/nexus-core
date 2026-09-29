from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, DateTime, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    
    # Soft Delete & Status Flag
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Зв'язок із результатами
    results: Mapped[list["Result"]] = relationship("Result", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(telegram_id={self.telegram_id}, role='{self.role}', active={self.is_active})>"


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options_json: Mapped[str] = mapped_column(Text, nullable=False)  # JSON-масив відповідей
    correct_option: Mapped[int] = mapped_column(nullable=False)
    
    # Soft Delete Flag (для приховування застарілих питань без фізичного видалення)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<QuizQuestion(id={self.id}, topic='{self.topic}', active={self.is_active})>"


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    passed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Зв'язок із користувачем
    user: Mapped["User"] = relationship("User", back_populates="results")

    def __repr__(self) -> str:
        return f"<Result(user_id={self.user_id}, topic='{self.topic}', score={self.score})>"
        