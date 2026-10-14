import pytest

from modules.health import HealthChecker


def test_get_system_status():
    """Перевірка синхронного збору метрик системи."""
    status = HealthChecker.get_system_status()

    assert status["status"] == "OK"
    assert "cpu_usage_percent" in status
    assert "ram" in status
    assert "disk" in status
    assert status["ram"]["percent"] >= 0


@pytest.mark.asyncio
async def test_async_get_status():
    """Перевірка асинхронного збору метрик системи."""
    status = await HealthChecker.async_get_status()

    assert status["status"] == "OK"
    assert isinstance(status["cpu_usage_percent"], float)
    assert status["disk"]["total_gb"] > 0
