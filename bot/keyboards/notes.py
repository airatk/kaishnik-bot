from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

def notes_chooser():
    notes_chooser_keyboard = InlineKeyboardMarkup()
    
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Показать", callback_data="show-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Добавить", callback_data="add-note"))
    notes_chooser_keyboard.row(InlineKeyboardButton(text="Удалить", callback_data="delete-note"))
    
    return notes_chooser_keyboard

def notes_list_dailer(notes, action):
    notes_list_dailer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    notes_list_dailer_keyboard.row(
        InlineKeyboardButton(
            text="{} все".format("Показать" if "show" in action else "Удалить"),
            callback_data="{}-all-notes".format("show" if "show" in action else "delete")
        )
    )
    
    notes_list_dailer_keyboard.add(*[
        InlineKeyboardButton(
            text="{note}{ellipsis}".format(
                note=notes[number][:25].replace("*", "").replace("_", "").replace("\\", ""),
                ellipsis="…" if len(notes[number]) > 25 else ""
            ),
            callback_data="{action}-{number}".format(
                number=number,
                action=action
            )
        ) for number in range(len(notes))
    ])
    
    return notes_list_dailer_keyboard
