from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(commands={"profile"})
async def show_profile(message: Message) -> None:
    """Display basic profile placeholder."""
    await message.answer("Ваш профиль пока пуст.")
