import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.logger import logger


class SecurityMiddleware(BaseMiddleware):
    """Мідлварь для Rate Limiting та базового аудиту безпеки в Aiogram 3.x."""

    def __init__(self, rate_limit: float = 1.0) -> None:
        super().__init__()
        self.rate_limit = (
            rate_limit  # мінімальний інтервал між повідомленнями в секундах
        )
        self.user_timestamps: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = time.time()

        # Перевірка Rate Limiting
        last_time = self.user_timestamps.get(user_id, 0.0)
        if current_time - last_time < self.rate_limit:
            logger.warning(
                f"Спроба спаму/часті запити від користувача {user_id}",
                extra={"security": True},
            )
            # Можна надіслати попередження або просто проігнорувати
            await event.answer(
                "⚠️ Занадто багато запитів. Будь ласка, зачекайте кілька секунд."
            )
            return

        self.user_timestamps[user_id] = current_time

        # Логування дії користувача (аудит)
        logger.info(f"Користувач {user_id} виконав команду/повідомлення: {event.text}")

        return await handler(event, data)
