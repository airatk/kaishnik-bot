from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.constants import BUILDINGS
from bot.constants import LIBRARIES
from bot.constants import DORMS

def choose_location_type():
    location_type_keyboard = InlineKeyboardMarkup()

    location_type_keyboard.row(InlineKeyboardButton(text="Учебные здания и СК", callback_data="buildings_type"))
    location_type_keyboard.row(InlineKeyboardButton(text="Библиотеки", callback_data="libraries_type"))
    location_type_keyboard.row(InlineKeyboardButton(text="Общежития", callback_data="dorms_type"))

    return location_type_keyboard

def buildings_dailer():
    buildings_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dailer_keyboard.add(*[
        InlineKeyboardButton(text=building, callback_data="buildings {}".format(building)) for building in BUILDINGS
    ])

    return buildings_dailer_keyboard

def libraries_dailer():
    libraries_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dailer_keyboard.add(*[
        InlineKeyboardButton(text=library, callback_data="libraries {}".format(library)) for library in LIBRARIES
    ])

    return libraries_dailer_keyboard

def dorms_dailer():
    dorms_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dailer_keyboard.add(*[
        InlineKeyboardButton(text=dorm, callback_data="dorms {}".format(dorm)) for dorm in DORMS
    ])

    return dorms_dailer_keyboard
