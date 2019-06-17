from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def delete_edit_chooser(edited_subjects):
    delete_edit_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    delete_edit_chooser_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    delete_edit_chooser_keyboard.row(InlineKeyboardButton(text="удалить все", callback_data="delete-edit-all"))
    
    delete_edit_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject.get_simple(),
            callback_data="delete-edit-number-{}".format(index)
        ) for index, subject in enumerate(edited_subjects)
    ])
    
    return delete_edit_chooser_keyboard
