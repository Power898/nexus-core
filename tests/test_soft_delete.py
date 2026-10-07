from datetime import datetime

import pytest
from sqlalchemy import select

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


@pytest.mark.asyncio
async def test_objects_manager_all_returns_only_active(db_session):
    """Перевірка того, що ObjectsManager.all() повертає тільки активні записи."""
    active_user = User(telegram_id=111111, username="active_user")
    deleted_user = User(telegram_id=222222, username="deleted_user")

    db_session.add_all([active_user, deleted_user])
    await db_session.commit()

    deleted_user.soft_delete()
    await db_session.commit()

    active_records = await User.objects.all(db_session)
    active_ids = [u.id for u in active_records]

    assert active_user.id in active_ids
    assert deleted_user.id not in active_ids


@pytest.mark.asyncio
async def test_objects_manager_all_with_deleted_returns_all(db_session):
    """Перевірка того, що ObjectsManager.all_with_deleted() повертає всі записи, включно з soft-deleted."""
    active_user = User(telegram_id=333333, username="active_user_2")
    deleted_user = User(telegram_id=444444, username="deleted_user_2")

    db_session.add_all([active_user, deleted_user])
    await db_session.commit()

    deleted_user.soft_delete()
    await db_session.commit()

    all_records = await User.objects.all_with_deleted(db_session)
    all_ids = [u.id for u in all_records]

    assert active_user.id in all_ids
    assert deleted_user.id in all_ids
