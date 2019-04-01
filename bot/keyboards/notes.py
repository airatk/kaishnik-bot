from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

def notes_chooser():
    notes_chooser_keyboard = InlineKeyboardMarkup()
    
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Показать все", callback_data="show-all-notes"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Показать одну", callback_data="show-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Добавить", callback_data="add-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Удалить одну", callback_data="delete-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Удалить все", callback_data="delete-all-notes"))
    
    return notes_chooser_keyboard

def notes_list_dailer(notes_number, action):
    notes_list_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    notes_list_dailer_keyboard.add(*[
        InlineKeyboardButton(
            text=number + 1,
            callback_data="{action}-{number}".format(
                number=number,
                action=action
            )
        ) for number in range(notes_number)
    ])
    
    return notes_list_dailer_keyboard
