import asyncio
from aiogram import Bot, Dispatcher

from app.config import get_settings
from app.routers.base import get_router


async def main() -> None:
    settings = get_settings()
    dp = Dispatcher()
    dp.include_router(get_router())
    bot = Bot(settings.bot_token, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
