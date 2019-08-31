from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.helpers.constants import INSTITUTES


def setup_way_chooser(is_old):
    setup_way_chooser_keyboard = InlineKeyboardMarkup()
    
    if is_old: setup_way_chooser_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-settings"))

    setup_way_chooser_keyboard.row(InlineKeyboardButton(text="с зачёткой", callback_data="settings-card-way"))
    setup_way_chooser_keyboard.row(InlineKeyboardButton(text="без зачётки", callback_data="settings-noncard-way"))

    return setup_way_chooser_keyboard


def cancel_option(row_width = 1):
    cancel_option_keyboard = InlineKeyboardMarkup(row_width=row_width)
    
    cancel_option_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-settings"))
    
    return cancel_option_keyboard


def institute_setter():
    institute_setter_keyboard = cancel_option()
    
    institute_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=institute,
            callback_data="set-institute-{}".format(institute_id)
        ) for institute_id, institute in INSTITUTES.items()
    ])
    
    return institute_setter_keyboard

def year_setter(years):
    year_setter_keyboard = cancel_option(row_width=2)
    
    year_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=year,
            callback_data="set-year-{}".format(year)
        ) for year in years
    ])
    
    return year_setter_keyboard

def group_number_setter(groups):
    group_number_setter_keyboard = cancel_option(row_width=2)
    
    group_number_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=group,
            callback_data="set-group-{}".format(group)
        ) for group in groups
    ])
    
    return group_number_setter_keyboard

def name_setter(names):
    name_setter_keyboard = cancel_option()
    
    name_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=name,
            callback_data="set-name-{}".format(name_id)
        ) for name, name_id in names.items()
    ])
    
    return name_setter_keyboard
