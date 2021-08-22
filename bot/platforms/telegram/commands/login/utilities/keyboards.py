from typing import List
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ChatType

from bot.platforms.telegram.commands.login.utilities.constants import MAX_ITEMS_NUMBER_ON_ONE_PAGE
from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.utilities.types import Command


def login_way_chooser(is_old: bool, chat_type: ChatType) -> InlineKeyboardMarkup:
    setup_way_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if is_old:
        setup_way_chooser_keyboard.row(cancel_button())
    
    if chat_type == ChatType.PRIVATE:
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="по логину-паролю от ББ", callback_data=Command.LOGIN_BB.value))
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="по номеру группы", callback_data=Command.LOGIN_COMPACT.value))
    else:
        setup_way_chooser_keyboard.row(InlineKeyboardButton(text="продолжить", callback_data=Command.LOGIN_COMPACT.value))
    
    return setup_way_chooser_keyboard


def againer() -> InlineKeyboardMarkup:
    againer_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    againer_keyboard.add(*[
        cancel_button(),
        InlineKeyboardButton(text="продолжить", callback_data=Command.LOGIN_COMPACT.value)
    ])
    
    return againer_keyboard

def guess_approver() -> InlineKeyboardMarkup:
    guess_approver_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    guess_approver_keyboard.row(cancel_button())
    
    guess_approver_keyboard.add(*[
        InlineKeyboardButton(text="нет", callback_data=Command.LOGIN_WRONG_GROUP_GUESS.value),
        InlineKeyboardButton(text="да", callback_data=Command.LOGIN_CORRECT_GROUP_GUESS.value),
    ])
    
    return guess_approver_keyboard
