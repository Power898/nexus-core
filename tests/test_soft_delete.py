from datetime import datetime

import pytest
from sqlalchemy import select

# Перевірте імпорт вашої моделі з SoftDeleteMixin (наприклад, User або інша)
from core.models import User


@pytest.mark.asyncio
async def test_soft_delete_lifecycle(db_session):
    """Перевірка життєвого циклу SoftDeleteMixin."""
    # 1. Створення тестового запису
    user = User(telegram_id=123456789, username="test_user")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.is_active is True
    assert user.deleted_at is None

    # 2. Викликаємо м'яке видалення
    user.soft_delete()
    await db_session.commit()
    await db_session.refresh(user)

    assert user.is_active is False
    assert user.deleted_at is not None
    assert isinstance(user.deleted_at, datetime)

    # 3. Перевірка, що видалений запис не потрапляє у вибірку активних
    stmt = select(User).where(User.is_active.is_(True))
    result = await db_session.execute(stmt)
    active_users = result.scalars().all()

    assert user not in active_users
