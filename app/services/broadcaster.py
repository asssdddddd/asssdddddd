from aiogram import Bot

from app.utils.text import render_listing


async def send_listing(bot: Bot, channel: str, listing: dict) -> None:
    """Send formatted listing to a channel."""
    text = render_listing(listing)
    await bot.send_message(channel, text)
