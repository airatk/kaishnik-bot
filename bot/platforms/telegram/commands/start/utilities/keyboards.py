from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.utilities.types import Command


def make_login() -> InlineKeyboardMarkup:
    make_login_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    make_login_keyboard.add(
        InlineKeyboardButton(text="войти как новый пользователь", callback_data=Command.LOGIN.value),
        InlineKeyboardButton(text="войти через ВК", callback_data=Command.LOGIN_PLATFORM.value)
    )
    
    return make_login_keyboard
