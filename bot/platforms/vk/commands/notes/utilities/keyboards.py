from typing import List

from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.keyboards import menu_button

from bot.models.note import Note

from bot.utilities.helpers import shorten
from bot.utilities.types import Command


def action_chooser(has_notes: bool) -> str:
    action_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    action_chooser_keyboard.add_text_button(text="Добавить", payload={ "callback": Command.NOTES_ADD.value })
    
    if has_notes:
        action_chooser_keyboard.add_row()
        action_chooser_keyboard.add_text_button(text="Показать", payload={ "callback": Command.NOTES_SHOW.value })
        
        action_chooser_keyboard.add_row()
        action_chooser_keyboard.add_text_button(text="Удалить", payload={ "callback": Command.NOTES_DELETE.value })
    
    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(**menu_button())
    
    return action_chooser_keyboard.get_keyboard()

def note_chooser(notes: List[Note], action: Command) -> str:
    note_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    note_chooser_keyboard.add_text_button(**menu_button())

    if len(notes) > 1:
        if action is Command.NOTES_SHOW:
            (text, color, callback_action) = ("Показать все", ButtonColor.PRIMARY, Command.NOTES_SHOW_ALL.value)
        elif action is Command.NOTES_DELETE:
            (text, color, callback_action) = ("Удалить все", ButtonColor.NEGATIVE, Command.NOTES_DELETE_ALL.value)
        
        note_chooser_keyboard.add_text_button(text=text, color=color, payload={ "callback": callback_action })
    
    for note in notes:
        note_chooser_keyboard.add_row()
        note_chooser_keyboard.add_text_button(
            text=shorten(note.text),
            color=ButtonColor.PRIMARY if action is not Command.NOTES_DELETE else ButtonColor.NEGATIVE,
            payload={
                action.value: "", 
                "note_id": note.note_id
            }
        )

    return note_chooser_keyboard.get_keyboard()
