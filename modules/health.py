import asyncio
from datetime import datetime, timezone

import psutil


class HealthChecker:
    """Модуль для моніторингу системних ресурсів NexusCore."""

    @staticmethod
    def get_system_status() -> dict:
        """Збирає базові метрики системи (CPU, RAM, Disk)."""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        cpu_percent = psutil.cpu_percent(interval=None)
        return {
            "status": "OK",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            # Додаємо дублювання ключів для сумісності з різними викликами (напр., тестами)
            "cpu_usage": cpu_percent,
            "cpu_usage_percent": cpu_percent,
            "memory_usage": memory.percent,
            "disk_usage": disk.percent,
            "ram": {
                "total_mb": round(memory.total / (1024 * 1024), 2),
                "used_mb": round(memory.used / (1024 * 1024), 2),
                "percent": memory.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent,
            },
        }

    @classmethod
    async def async_get_status(cls) -> dict:
        """Асинхронна обгортка для уникнення блокування event loop."""
        return await asyncio.to_thread(cls.get_system_status)

    @classmethod
    async def get_system_health(cls) -> dict:
        """Аліас для сумісності з обробниками команд та тестами."""
        return await cls.async_get_status()
