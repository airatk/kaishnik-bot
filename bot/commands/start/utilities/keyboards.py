from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.commands import Commands


def make_login() -> InlineKeyboardMarkup:
    make_login_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    
    make_login_keyboard.row(InlineKeyboardButton(text="/login", callback_data=Commands.LOGIN.value))
    
    return make_login_keyboard
