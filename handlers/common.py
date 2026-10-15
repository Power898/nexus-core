import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from adapters.rbac import require_role
from modules.health import HealthChecker

# Налаштовуємо логер для цього модуля
logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Обробник команди /start."""
    await message.answer(
        "👋 Вітаю! <b>NexusCore</b> успішно ініціалізовано.\n"
        "Система працює у захищеному режимі (Security by Design). 🛡️"
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обробник команди /help."""
    await message.answer(
        "📋 <b>Доступні команди:</b>\n"
        "/start — Запуск бота\n"
        "/health — Перевірка стану системи (CPU, RAM, Disk)\n"
        "/help — Показать цю довідку"
    )


@router.message(Command("health"))
@require_role("tenant_admin")  # Захищаємо команду, вимагаючи привілейовану роль
async def cmd_health(message: Message) -> None:
    """Обробник команди /health для моніторингу через HealthChecker."""
    try:
        health_data = await HealthChecker.get_system_health()

        status_msg = (
            "🟢 <b>System Health Report:</b>\n"
            f"• <b>CPU Usage:</b> {health_data.get('cpu_usage', 'N/A')}%\n"
            f"• <b>Memory Usage:</b> {health_data.get('memory_usage', 'N/A')}%\n"
            f"• <b>Disk Usage:</b> {health_data.get('disk_usage', 'N/A')}%\n"
            f"• <b>Status:</b> {health_data.get('status', 'OK')}"
        )
        await message.answer(status_msg)
    except (ConnectionError, TimeoutError, OSError) as e:
        # Логуємо технічну деталь для адміністратора/розробника
        logger.error("Системна помилка під час збору метрик здоров'я: %s", e)
        # Користувачу відправляємо зрозумілу і безпечну відповідь
        await message.answer(
            "❌ Не вдалося отримати показники системи через технічну проблему."
        )
