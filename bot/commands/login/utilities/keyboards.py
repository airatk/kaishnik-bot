from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.keyboards import cancel_button
from bot.shared.api.constants import INSTITUTES
from bot.shared.commands import Commands


def login_way_chooser(is_old: bool) -> InlineKeyboardMarkup:
    setup_way_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if is_old: setup_way_chooser_keyboard.row(cancel_button())
    
    setup_way_chooser_keyboard.row(InlineKeyboardButton(text="с зачёткой", callback_data=Commands.LOGIN_EXTENDED.value))
    setup_way_chooser_keyboard.row(InlineKeyboardButton(text="без зачётки", callback_data=Commands.LOGIN_COMPACT.value))
    
    return setup_way_chooser_keyboard


def institute_setter() -> InlineKeyboardMarkup:
    institute_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    institute_setter_keyboard.row(cancel_button())
    
    institute_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=institute, callback_data=" ".join([ Commands.LOGIN_SET_INSTITUTE.value, institute_id ])
        ) for (institute_id, institute) in INSTITUTES.items()
    ])
    
    return institute_setter_keyboard

def year_setter(years: {str: str}) -> InlineKeyboardMarkup:
    year_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    year_setter_keyboard.row(cancel_button())
    
    year_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=year, callback_data=" ".join([ Commands.LOGIN_SET_YEAR.value, year ])
        ) for year in years
    ])
    
    return year_setter_keyboard

def group_number_setter(groups: {str: str}) -> InlineKeyboardMarkup:
    group_number_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)
    
    group_number_setter_keyboard.row(cancel_button())
    
    group_number_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=group, callback_data=" ".join([ Commands.LOGIN_SET_GROUP.value, group ])
        ) for group in groups
    ])
    
    return group_number_setter_keyboard

def name_setter(names: {str: str}) -> InlineKeyboardMarkup:
    name_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    name_setter_keyboard.row(cancel_button())
    
    name_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=name, callback_data=" ".join([ Commands.LOGIN_SET_NAME.value, name_id ])
        ) for (name, name_id) in names.items()
    ])
    
    return name_setter_keyboard
