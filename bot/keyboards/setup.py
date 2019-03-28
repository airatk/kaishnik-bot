from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton

from bot.constants import INSTITUTES

def institute_setter():
    institute_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    institute_setter_keyboard.add(*[
        KeyboardButton(text=institute) for institute in INSTITUTES
    ])

    return institute_setter_keyboard

def year_setter(years):
    year_setter_keyboard = ReplyKeyboardMarkup(row_width=6, resize_keyboard=True)

    year_setter_keyboard.add(*[
        KeyboardButton(text=year) for year in years
    ])

    return year_setter_keyboard

def group_number_setter(groups):
    group_number_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    group_number_setter_keyboard.add(*[
        KeyboardButton(text=group) for group in groups
    ])

    return group_number_setter_keyboard

def name_setter(names):
    name_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    name_setter_keyboard.add(*[
        KeyboardButton(text=name) for name in names
    ])

    return name_setter_keyboard
