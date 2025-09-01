from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.common import main_menu


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Greet user and show main menu."""
    await message.answer("Добро пожаловать в Prorab!", reply_markup=main_menu("worker"))
