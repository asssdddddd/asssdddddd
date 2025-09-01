from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(role: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Моя роль", callback_data="role")],
        [InlineKeyboardButton(text="Опубликовать объявление", callback_data="publish")],
        [InlineKeyboardButton(text="Просмотреть канал", callback_data=f"view:{role}")],
        [InlineKeyboardButton(text="Мой профиль", callback_data="profile")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
