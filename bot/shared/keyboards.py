from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.shared.commands import Commands


def cancel_option(row_width = 1):
    cancel_option_keyboard = InlineKeyboardMarkup(row_width=row_width)
    
    cancel_option_keyboard.row(InlineKeyboardButton(text="отменить", callback_data=Commands.CANCEL.value))
    
    return cancel_option_keyboard
