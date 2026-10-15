from unittest.mock import AsyncMock, MagicMock

import pytest

from adapters.rbac import require_role


@pytest.mark.asyncio
async def test_require_role_allowed():
    """Тест: доступ дозволено, якщо роль користувача достатня."""

    # Створюємо тестовий хендлер із декоратором
    @require_role("tenant_admin")
    async def mock_handler(message):
        return "success"

    # Мокаємо повідомлення від користувача з роллю tenant_admin
    message = MagicMock()
    message.from_user.id = 123

    # Викликаємо хендлер із передачею ролі у kwargs
    result = await mock_handler(message, user_role="tenant_admin")
    assert result == "success"


@pytest.mark.asyncio
async def test_require_role_denied():
    """Тест: доступ заблоковано, якщо роль користувача занизька."""

    @require_role("tenant_admin")
    async def mock_handler(message):
        return "success"

    # Мокаємо повідомлення від звичайного користувача (role: user)
    message = MagicMock()
    message.from_user.id = 456
    message.answer = AsyncMock()

    # Викликаємо хендлер із занизькою роллю
    result = await mock_handler(message, user_role="user")

    # Перевіряємо, що виконання зупинилося і надіслано сповіщення про помилку
    assert result is None
    message.answer.assert_awaited_once_with(
        "❌ У вас недостатньо прав для виконання цієї команди."
    )
