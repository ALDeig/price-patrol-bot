from typing import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from price_patrol_bot.src.services.db.models import MStore


def kb_select_store(stores: Sequence[MStore]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=store.name, callback_data=f"store:{store.id}")]
        for store in stores
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
