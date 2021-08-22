from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.models.note import Note

from bot.utilities.constants import MAX_SYMBOLS_NUMBER
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Command


def action_chooser(has_notes: bool) -> InlineKeyboardMarkup:
    action_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    action_chooser_keyboard.row(cancel_button())
    
    action_chooser_keyboard.row(InlineKeyboardButton(text="добавить", callback_data=Command.NOTES_ADD.value))
    
    if has_notes:
        action_chooser_keyboard.row(InlineKeyboardButton(text="показать", callback_data=Command.NOTES_SHOW.value))
        action_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data=Command.NOTES_DELETE.value))
    
    return action_chooser_keyboard

def note_chooser(notes: List[Note], action: Command) -> InlineKeyboardMarkup:
    note_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if len(notes) > 1:
        if action is Command.NOTES_SHOW:
            (text, callback_action) = ("показать все", Command.NOTES_SHOW_ALL.value)
        elif action is Command.NOTES_DELETE:
            (text, callback_action) = ("удалить все", Command.NOTES_DELETE_ALL.value)
        
        note_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(text=text, callback_data=callback_action)
        )
    else:
        note_chooser_keyboard.row(cancel_button())
    
    note_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text="{note}{ellipsis}".format(
                note=remove_markdown(note.text[:MAX_SYMBOLS_NUMBER]).strip(),
                ellipsis="…" if len(note.text) > MAX_SYMBOLS_NUMBER else ""
            ),
            callback_data=" ".join([ action.value, str(note.note_id) ])
        ) for note in notes
    ])
    
    return note_chooser_keyboard
