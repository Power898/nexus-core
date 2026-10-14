from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import Message

from handlers.common import cmd_health, cmd_help, cmd_start


@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()  # Робимо метод асинхронним
    await cmd_start(message)
    message.answer.assert_awaited_once()
    args, _ = message.answer.call_args
    assert "NexusCore" in args[0]


@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()  # Робимо метод асинхронним
    await cmd_help(message)
    message.answer.assert_awaited_once()
    args, _ = message.answer.call_args
    assert "Доступні команди" in args[0]


@pytest.mark.asyncio
async def test_cmd_health_success():
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()  # Робимо метод асинхронним

    fake_health = {
        "cpu_usage": 15.0,
        "memory_usage": 50.0,
        "disk_usage": 40.0,
        "status": "OK",
    }

    # Замініть HealthChecker.get_system_health на реальну назву методу з modules/health.py якщо вона відрізняється
    with patch(
        "handlers.common.HealthChecker.get_system_health",
        new=AsyncMock(return_value=fake_health),
    ):
        await cmd_health(message)

    message.answer.assert_awaited_once()
    args, _ = message.answer.call_args
    assert "System Health Report" in args[0]
    assert "15.0%" in args[0]
