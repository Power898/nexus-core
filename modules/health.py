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

        return {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu_usage_percent": psutil.cpu_percent(interval=None),
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
