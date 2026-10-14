from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message, User

from adapters.base_adapter import BaseAdapter
from adapters.middleware import SecurityMiddleware


class DummyAdapter(BaseAdapter):
    """Тестова реалізація адаптера для перевірки базового класу."""

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def send_message(self, recipient_id: int | str, text: str, **kwargs) -> None:
        pass


@pytest.mark.asyncio
async def test_base_adapter_inheritance():
    adapter = DummyAdapter()
    assert isinstance(adapter, BaseAdapter)


@pytest.mark.asyncio
async def test_security_middleware_rate_limit():
    middleware = SecurityMiddleware(rate_limit=1.0)

    # Створюємо мок для Message та робимо answer асинхронним
    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = User(id=123, is_bot=False, first_name="Test")
    mock_message.text = "/health"
    mock_message.answer = AsyncMock()  # Явно робимо метод answer асинхронним моком

    handler = AsyncMock(return_value="OK")

    # Перший виклик — має пройти успішно
    result1 = await middleware(handler, mock_message, {})
    assert result1 == "OK"

    # Другий виклик одразу ж — має спрацювати rate limit (поверне None і викличе answer)
    result2 = await middleware(handler, mock_message, {})
    assert result2 is None
    mock_message.answer.assert_awaited_once()
