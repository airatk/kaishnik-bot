from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

def make_send(command):
    return ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton(text=command))

def skipper(text, callback_data):
    skipper_keyboard = InlineKeyboardMarkup()
    skipper_keyboard.row(InlineKeyboardButton(text=text, callback_data=callback_data))

    return skipper_keyboard
