from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.shared.commands import Commands


def make_login():
    make_login_keyboard = InlineKeyboardMarkup()
    
    make_login_keyboard.row(InlineKeyboardButton(text="/login", callback_data=Commands.LOGIN.value))
    
    return make_login_keyboard
