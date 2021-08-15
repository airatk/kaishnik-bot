from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.models.notes import Notes

from bot.utilities.constants import MAX_SYMBOLS_NUMBER
from bot.utilities.types import Commands


def action_chooser(has_notes: bool) -> InlineKeyboardMarkup:
    action_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    action_chooser_keyboard.row(cancel_button())
    
    action_chooser_keyboard.row(InlineKeyboardButton(text="добавить", callback_data=Commands.NOTES_ADD.value))
    
    if has_notes:
        action_chooser_keyboard.row(InlineKeyboardButton(text="показать", callback_data=Commands.NOTES_SHOW.value))
        action_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data=Commands.NOTES_DELETE.value))
    
    return action_chooser_keyboard

def note_chooser(notes: List[Notes], action: Commands) -> InlineKeyboardMarkup:
    note_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if notes.count() > 1:
        if action is Commands.NOTES_SHOW:
            (text, callback_action) = ("показать все", Commands.NOTES_SHOW_ALL.value)
        elif action is Commands.NOTES_DELETE:
            (text, callback_action) = ("удалить все", Commands.NOTES_DELETE_ALL.value)
        
        note_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(text=text, callback_data=callback_action)
        )
    else:
        note_chooser_keyboard.row(cancel_button())
    
    note_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text="{note}{ellipsis}".format(
                note=note.note[:MAX_SYMBOLS_NUMBER].strip().replace("*", "").replace("_", "").replace("\\", ""),
                ellipsis="…" if len(note.note) > MAX_SYMBOLS_NUMBER else ""
            ),
            callback_data=" ".join([ action.value, str(note.note_id) ])
        ) for note in notes
    ])
    
    return note_chooser_keyboard
