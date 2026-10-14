from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from adapters.base_adapter import BaseAdapter
from core.logger import logger


class TelegramAdapter(BaseAdapter):
    """Адаптер для роботи з Telegram API на базі Aiogram 3.x."""

    def __init__(self, token: str) -> None:
        self.token = token
        self.bot = Bot(
            token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()
        logger.info("TelegramAdapter ініціалізовано.")

    async def start(self) -> None:
        """Запуск Telegram-бота в режимі polling."""
        logger.info("Запуск Telegram-бота (Polling)...")
        # Тут згодом підключимо роутери, мідлварі та запустимо polling
        # Наразі готуємо каркас диспетчера
        await self.dp.start_polling(self.bot)

    async def stop(self) -> None:
        """Коректна зупинка бота та закриття сесії."""
        logger.info("Зупинка Telegram-бота...")
        await self.bot.session.close()

    async def send_message(
        self, recipient_id: int | str, text: str, **kwargs: Any
    ) -> None:
        """Надсилання текстового повідомлення користувачу в Telegram."""
        try:
            await self.bot.send_message(chat_id=recipient_id, text=text, **kwargs)
            logger.info(f"Повідомлення успішно надіслано користувачу {recipient_id}")
        except Exception as e:
            logger.error(f"Помилка надсилання повідомлення для {recipient_id}: {e}")
            raise
