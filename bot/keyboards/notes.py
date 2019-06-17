from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def notes_chooser():
    notes_chooser_keyboard = InlineKeyboardMarkup()
    
    notes_chooser_keyboard.row(InlineKeyboardButton(text="показать", callback_data="show-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="добавить", callback_data="add-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data="delete-note"))
    
    return notes_chooser_keyboard

def notes_list_dialer(notes, action):
    notes_list_dialer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    notes_list_dialer_keyboard.row(
        InlineKeyboardButton(
            text="{} все".format("Показать" if "show" in action else "Удалить"),
            callback_data="{}-all-notes".format("show" if "show" in action else "delete")
        )
    )
    
    notes_list_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text="{note}{ellipsis}".format(
                note=note[:25].replace("*", "").replace("_", "").replace("\\", ""),
                ellipsis="…" if len(note) > 25 else ""
            ),
            callback_data="{action}-{number}".format(
                number=number,
                action=action
            )
        ) for number, note in enumerate(notes)
    ])
    
    return notes_list_dialer_keyboard
