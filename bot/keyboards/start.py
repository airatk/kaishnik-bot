from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def make_setup():
    make_setup_keyboard = InlineKeyboardMarkup()

    make_setup_keyboard.row(InlineKeyboardButton(text="/settings", callback_data="first-setup"))

    return make_setup_keyboard
