from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from handlers.common import cmd_health, cmd_help, cmd_start


@pytest.mark.asyncio
async def test_cmd_start():
    message = MagicMock()
    message.answer = AsyncMock()
    await cmd_start(message)
    message.answer.assert_awaited_once()
    args, _ = message.answer.call_args
    assert "NexusCore" in args[0]


@pytest.mark.asyncio
async def test_cmd_help():
    message = MagicMock()
    message.answer = AsyncMock()
    await cmd_help(message)
    message.answer.assert_awaited_once()
    args, _ = message.answer.call_args
    assert "Доступні команди" in args[0]


@pytest.mark.asyncio
async def test_cmd_health_success():
    message = MagicMock()
    message.from_user.id = 123  # Тепер MagicMock спокійно створить цей атрибут
    message.answer = AsyncMock()

    fake_health = {
        "cpu_usage": 15.0,
        "memory_usage": 50.0,
        "disk_usage": 40.0,
        "status": "OK",
    }

    with patch(
        "handlers.common.HealthChecker.get_system_health",
        new=AsyncMock(return_value=fake_health),
    ):
        await cmd_health(message, user_role="tenant_admin")

    message.answer.assert_awaited_once()
    args, _ = message.answer.call_args
    assert "System Health Report" in args[0]
    assert "15.0%" in args[0]
