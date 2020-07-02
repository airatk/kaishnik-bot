from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ChatType

from bot.shared.keyboards import cancel_button
from bot.shared.api.constants import INSTITUTES
from bot.shared.commands import Commands


def login_way_chooser(is_old: bool, chat_type: ChatType) -> InlineKeyboardMarkup:
    setup_way_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if is_old: setup_way_chooser_keyboard.row(cancel_button())
    
    if chat_type == ChatType.PRIVATE:
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="с зачёткой", callback_data=Commands.LOGIN_EXTENDED.value))
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="без зачётки", callback_data=Commands.LOGIN_COMPACT.value))
    else:
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="продолжить", callback_data=Commands.LOGIN_COMPACT.value))
    
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

def group_setter(groups: {str: str}) -> InlineKeyboardMarkup:
    group_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)
    
    group_setter_keyboard.row(cancel_button())
    
    group_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=group, callback_data=" ".join([ Commands.LOGIN_SET_GROUP.value, group, group_id ])
        ) for (group, group_id) in groups.items()
    ])
    
    return group_setter_keyboard

def name_setter(names: {str: str}) -> InlineKeyboardMarkup:
    name_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    name_setter_keyboard.row(cancel_button())
    
    name_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=name, callback_data=" ".join([ Commands.LOGIN_SET_NAME.value, name_id ])
        ) for (name, name_id) in names.items()
    ])
    
    return name_setter_keyboard


def againer() -> InlineKeyboardMarkup:
    againer_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    againer_keyboard.add(*[
        cancel_button(),
        InlineKeyboardButton(text="продолжить", callback_data=Commands.LOGIN_COMPACT.value)
    ])
    
    return againer_keyboard

def guess_approver() -> InlineKeyboardMarkup:
    guess_approver_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    guess_approver_keyboard.row(cancel_button())
    
    guess_approver_keyboard.add(*[
        InlineKeyboardButton(text="нет", callback_data=Commands.LOGIN_WRONG_GROUP_GUESS.value),
        InlineKeyboardButton(text="да", callback_data=Commands.LOGIN_CORRECT_GROUP_GUESS.value),
    ])
    
    return guess_approver_keyboard
