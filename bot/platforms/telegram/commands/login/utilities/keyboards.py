from typing import List
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ChatType

from bot.platforms.telegram.commands.login.utilities.constants import MAX_ITEMS_NUMBER_ON_ONE_PAGE
from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.utilities.types import Commands
from bot.utilities.api.constants import INSTITUTES


def login_way_chooser(is_old: bool, chat_type: ChatType) -> InlineKeyboardMarkup:
    setup_way_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if is_old:
        setup_way_chooser_keyboard.row(cancel_button())
    
    if chat_type == ChatType.PRIVATE:
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="без зачётки", callback_data=Commands.LOGIN_COMPACT.value))
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="с зачёткой", callback_data=Commands.LOGIN_EXTENDED.value))
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

def year_setter(years: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
    year_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    year_setter_keyboard.row(cancel_button())

    year_setter_keyboard.add(*[
        InlineKeyboardButton(
            text=year, callback_data=" ".join([ Commands.LOGIN_SET_YEAR.value, year ])
        ) for (year, _) in years
    ])
    
    return year_setter_keyboard

def group_setter(groups: List[Tuple[str, str]], offset: int = 0) -> InlineKeyboardMarkup:
    group_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    group_setter_keyboard.row(cancel_button())
    
    if offset > 0:
        if offset < (len(groups) - MAX_ITEMS_NUMBER_ON_ONE_PAGE):
            group_setter_keyboard.add(
                InlineKeyboardButton(
                    text="назад", callback_data=" ".join([ Commands.LOGIN_GROUPS_PREVIOUS_PAGE.value, str(offset - MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
                ),
                InlineKeyboardButton(
                    text="вперёд", callback_data=" ".join([ Commands.LOGIN_GROUPS_NEXT_PAGE.value, str(offset + MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
                )
            )
        else:
            group_setter_keyboard.add(
                InlineKeyboardButton(
                    text="назад", callback_data=" ".join([ Commands.LOGIN_GROUPS_PREVIOUS_PAGE.value, str(offset - MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
                )
            )
    elif len(groups) != MAX_ITEMS_NUMBER_ON_ONE_PAGE:
        group_setter_keyboard.add(
            InlineKeyboardButton(
                text="вперёд", callback_data=" ".join([ Commands.LOGIN_GROUPS_NEXT_PAGE.value, str(offset + MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
            )
        )
    
    for (group, group_id) in groups[offset:(offset + MAX_ITEMS_NUMBER_ON_ONE_PAGE)]:
        group_setter_keyboard.row(
            InlineKeyboardButton(
                text=group, callback_data=" ".join([ Commands.LOGIN_SET_GROUP.value, group, group_id ])
            )
        )

    return group_setter_keyboard

def name_setter(names: List[Tuple[str, str]], offset: int = 0) -> InlineKeyboardMarkup:
    name_setter_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)

    name_setter_keyboard.row(cancel_button())
    
    if offset > 0:
        if offset < (len(names) - MAX_ITEMS_NUMBER_ON_ONE_PAGE):
            name_setter_keyboard.add(
                InlineKeyboardButton(
                    text="назад", callback_data=" ".join([ Commands.LOGIN_NAMES_PREVIOUS_PAGE.value, str(offset - MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
                ),
                InlineKeyboardButton(
                    text="вперёд", callback_data=" ".join([ Commands.LOGIN_NAMES_NEXT_PAGE.value, str(offset + MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
                )
            )
        else:
            name_setter_keyboard.add(
                InlineKeyboardButton(
                    text="назад", callback_data=" ".join([ Commands.LOGIN_NAMES_PREVIOUS_PAGE.value, str(offset - MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
                )
            )
    elif len(names) != MAX_ITEMS_NUMBER_ON_ONE_PAGE:
        name_setter_keyboard.add(
            InlineKeyboardButton(
                text="вперёд", callback_data=" ".join([ Commands.LOGIN_NAMES_NEXT_PAGE.value, str(offset + MAX_ITEMS_NUMBER_ON_ONE_PAGE) ])
            )
        )
    
    for (name_id, name) in names[offset:(offset + MAX_ITEMS_NUMBER_ON_ONE_PAGE)]:
        name_setter_keyboard.row(
            InlineKeyboardButton(
                text=name, callback_data=" ".join([ Commands.LOGIN_SET_NAME.value, name_id ])
            )
        )
    
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
