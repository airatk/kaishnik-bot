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

def buildings_dialer():
    buildings_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=building,
            callback_data="buildings {}".format(building)
        ) for building in BUILDINGS
    ])

    return buildings_dialer_keyboard

def libraries_dialer():
    libraries_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=library,
            callback_data="libraries {}".format(library)
        ) for library in LIBRARIES
    ])

    return libraries_dialer_keyboard

def dorms_dialer():
    dorms_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=dorm,
            callback_data="dorms {}".format(dorm)
        ) for dorm in DORMS
    ])

    return dorms_dialer_keyboard
