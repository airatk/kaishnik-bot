from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardRemove

from constants import buildings
from constants import libraries
from constants import dorms

# /classes
def schedule_type():
    schedule_type_keyboard = InlineKeyboardMarkup()

    schedule_type_keyboard.row(
        InlineKeyboardButton(text="сегодня", callback_data="today's"),
        InlineKeyboardButton(text="завтра", callback_data="tomorrow's")
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю", callback_data="weekly current"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю", callback_data="weekly next"))

    return schedule_type_keyboard

# /locations
def choose_location_type():
    location_type_keyboard = InlineKeyboardMarkup()

    location_type_keyboard.row(InlineKeyboardButton(text="Учебные здания и СК", callback_data="buildings"))
    location_type_keyboard.row(InlineKeyboardButton(text="Библиотеки", callback_data="libraries"))
    location_type_keyboard.row(InlineKeyboardButton(text="Общежития", callback_data="dorms"))

    return location_type_keyboard

def buildings_dailer():
    buildings_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dailer_keyboard.add(*[
        InlineKeyboardButton(text="{b_}".format(b_=b_), callback_data="b_s {b_}".format(b_=b_)) for b_ in buildings.keys()
    ])

    return buildings_dailer_keyboard

def libraries_dailer():
    libraries_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dailer_keyboard.add(*[
        InlineKeyboardButton(text="{l_}".format(l_=l_), callback_data="l_s {l_}".format(l_=l_)) for l_ in libraries.keys()
    ])

    return libraries_dailer_keyboard

def dorms_dailer():
    dorms_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dailer_keyboard.add(*[
        InlineKeyboardButton(text="{d_}".format(d_=d_), callback_data="d_s {d_}".format(d_=d_)) for d_ in dorms.keys()
    ])

    return dorms_dailer_keyboard

# /settings
def settings_entry():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton(text="/settings"))

# Remove keyboard
def remove_keyboard():
    return ReplyKeyboardRemove()
