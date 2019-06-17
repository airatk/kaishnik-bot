from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def edit_chooser():
    edit_chooser_keyboard = InlineKeyboardMarkup()
    
    edit_chooser_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    edit_chooser_keyboard.row(InlineKeyboardButton(text="изменить", callback_data="add-edit"))
    edit_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data="delete-edit"))
    
    return edit_chooser_keyboard


def edit_canceler():
    edit_canceler_keyboard = InlineKeyboardMarkup()
    
    edit_canceler_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    return edit_canceler_keyboard

def canceler_skipper(callback_data):
    canceler_skipper_keyboard = InlineKeyboardMarkup()
    
    canceler_skipper_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    canceler_skipper_keyboard.row(InlineKeyboardButton(text="пропустить", callback_data=callback_data))
    
    return canceler_skipper_keyboard
