from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


publish_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать", callback_data="confirm")],
        [InlineKeyboardButton(text="Изменить", callback_data="edit")],
    ]
)
