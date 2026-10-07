import pytest
from sqlalchemy import select

from core.models import Result, User


@pytest.mark.asyncio
async def test_objects_manager_all(db_session, sample_user):
    """ObjectsManager.all() — повертає тільки активні записи."""
    deleted_user = User(
        telegram_id=999999,
        username="deleted_user",
    )
    if hasattr(deleted_user, "active"):
        deleted_user.active = False
    elif hasattr(deleted_user, "is_active"):
        deleted_user.is_active = False

    db_session.add(deleted_user)
    await db_session.commit()

    users = await User.objects.all(db_session)
    user_ids = [u.id for u in users]

    assert sample_user.id in user_ids
    assert deleted_user.id not in user_ids


@pytest.mark.asyncio
async def test_objects_manager_filter(db_session, sample_user, admin_user):
    """ObjectsManager.filter() — фільтрує лише активні записи."""
    deleted_admin = User(
        telegram_id=888888,
        username="deleted_admin",
        role="admin",
    )
    if hasattr(deleted_admin, "active"):
        deleted_admin.active = False
    elif hasattr(deleted_admin, "is_active"):
        deleted_admin.is_active = False

    db_session.add(deleted_admin)
    await db_session.commit()

    admin_users = await User.objects.filter(db_session, User.role == "admin")
    admin_ids = [u.id for u in admin_users]

    assert admin_user.id in admin_ids
    assert deleted_admin.id not in admin_ids


@pytest.mark.asyncio
async def test_objects_manager_all_with_deleted(db_session, sample_user):
    """ObjectsManager.all_with_deleted() — повертає всі записи, включно з soft-deleted."""
    deleted_user = User(
        telegram_id=777777,
        username="soft_deleted",
    )
    if hasattr(deleted_user, "active"):
        deleted_user.active = False
    elif hasattr(deleted_user, "is_active"):
        deleted_user.is_active = False

    db_session.add(deleted_user)
    await db_session.commit()

    all_users = await User.objects.all_with_deleted(db_session)
    all_ids = [u.id for u in all_users]

    assert sample_user.id in all_ids
    assert deleted_user.id in all_ids


@pytest.mark.asyncio
async def test_user_result_relationship_and_cascade(db_session, sample_user):
    """ORM зв'язок між User та Result та перевірка каскадного видалення."""
    result = Result(
        user_id=sample_user.id,
        topic="General",
        score=10,
    )
    db_session.add(result)
    await db_session.commit()
    await db_session.refresh(result)

    assert result.user_id == sample_user.id

    # Перевіряємо каскадне видалення
    await db_session.delete(sample_user)
    await db_session.commit()

    stmt = select(Result).where(Result.id == result.id)
    res = await db_session.execute(stmt)
    fetched_result = res.scalar_one_or_none()

    assert fetched_result is None
