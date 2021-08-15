from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.utilities.types import Commands


def make_login() -> InlineKeyboardMarkup:
    make_login_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    
    make_login_keyboard.row(InlineKeyboardButton(text="войти", callback_data=Commands.LOGIN.value))
    make_login_keyboard.row(InlineKeyboardButton(text="войти через ВК", callback_data=Commands.LOGIN_PLATFORM.value))

    return make_login_keyboard
