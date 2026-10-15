from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from aiogram.types import Message

from core.logger import logger

# Визначення рівнів ролей для ієрархічної перевірки
ROLE_HIERARCHY = {
    "user": 1,
    "tenant_admin": 2,
    "system_admin": 3,
}


def require_role(required_role: str) -> Callable:
    """
    Декоратор для перевірки ролей (RBAC) у хендлерах Telegram-бота.
    Порівнює рівень прав користувача з мінімально необхідною роллю.
    """

    def decorator(
        handler: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(handler)
        async def wrapper(message: Message, *args: Any, **kwargs: Any) -> Any:
            user_id = message.from_user.id if message.from_user else 0

            # Витягуємо роль користувача і видаляємо її з kwargs,
            # щоб вона не передавалася далі в хендлер і не ламала сигнатуру
            user_role = kwargs.pop("user_role", "user")

            user_level = ROLE_HIERARCHY.get(user_role, 0)
            required_level = ROLE_HIERARCHY.get(required_role, 1)

            if user_level < required_level:
                logger.warning(
                    f"⛔ Несанкціонований доступ! Користувач {user_id} з роллю '{user_role}' "
                    f"намагався виконати захищену дію (потрібна роль: '{required_role}').",
                    extra={"security": True},
                )
                await message.answer(
                    "❌ У вас недостатньо прав для виконання цієї команди."
                )
                return

            logger.info(
                f"✅ Доступ дозволено для користувача {user_id} (роль: '{user_role}')."
            )
            return await handler(message, *args, **kwargs)

        return wrapper

    return decorator
