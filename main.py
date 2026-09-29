import asyncio
import sys
from aiogram import Bot, Dispatcher
from config.settings import settings
from core.database import init_db
from core.logger import logger


async def main() -> None:
    logger.info("Запуск системи NexusCore...")

    # 1. Ініціалізація бази даних та створення таблиць
    await init_db()

    # 2. Перевірка наявності токена бота
    if not settings.BOT_TOKEN or settings.BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error("BOT_TOKEN не вказано у файлі .env! Запуск зупинено.")
        sys.exit(1)

    # 3. Створення екземплярів Bot та Dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    logger.info("NexusCore Engine успішно запущено. Очікування запитів...")

    try:
        # Пропуск накопичених оновлень та запуск polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критична помилка під час роботи бота: {e}")
    finally:
        await bot.session.close()
        logger.info("Сесію бота закрито. NexusCore зупинено.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("NexusCore зупинено користувачем.")