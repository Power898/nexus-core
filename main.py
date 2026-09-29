import asyncio
import sys

from aiogram import Bot, Dispatcher

from config.settings import settings
from core.database import init_db
from core.logger import logger


async def main() -> None:
    logger.info("Запуск системи NexusCore...")

    # 1. Ініціалізація бази даних
    await init_db()

    # 2. Перевірка токена
    if not settings.BOT_TOKEN or settings.BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error("BOT_TOKEN не вказано у файлі .env! Запуск зупинено.")
        sys.exit(1)

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    logger.info("NexusCore Engine успішно запущено. Очікування запитів...")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception:  # noqa: BLE001
        logger.exception("Критична помилка під час роботи бота")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("NexusCore зупинено користувачем.")
