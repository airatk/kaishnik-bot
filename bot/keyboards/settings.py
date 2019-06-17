from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.helpers.constants import INSTITUTES


def institute_setter(is_old):
    institute_setter_keyboard = InlineKeyboardMarkup(row_width=1)
    
    if is_old: institute_setter_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-settings"))
    
    institute_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=institute,
            callback_data="set-institute-{}".format(institute_id)
        ) for institute_id, institute in INSTITUTES.items()
    ])
    
    return institute_setter_keyboard

def year_setter(years):
    year_setter_keyboard = InlineKeyboardMarkup(row_width=2)
    
    year_setter_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-settings"))
    
    year_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=year,
            callback_data="set-year-{}".format(year)
        ) for year in years
    ])
    
    return year_setter_keyboard

def group_number_setter(groups):
    group_number_setter_keyboard = InlineKeyboardMarkup(row_width=2)
    
    group_number_setter_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-settings"))
    
    group_number_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=group,
            callback_data="set-group-{}".format(group)
        ) for group in groups
    ])
    
    return group_number_setter_keyboard

def name_setter(names):
    name_setter_keyboard = InlineKeyboardMarkup(row_width=1)
    
    name_setter_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-settings"))
    
    name_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=name,
            callback_data="set-name-{}".format(name_id)
        ) for name, name_id in names.items()
    ])
    
    return name_setter_keyboard

def set_card_skipper():
    set_card_skipper_keyboard = InlineKeyboardMarkup()
    
    set_card_skipper_keyboard.row(InlineKeyboardButton(text="пропустить", callback_data="skip-set-card"))
    
    return set_card_skipper_keyboard
