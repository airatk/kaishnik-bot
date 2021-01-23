from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.utilities.types import Commands


def cancel_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="отменить", callback_data=Commands.CANCEL.value)

def canceler(row_width: int = 1) -> InlineKeyboardMarkup:
    canceler_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=row_width)
    
    canceler_keyboard.row(cancel_button())
    
    return canceler_keyboard
