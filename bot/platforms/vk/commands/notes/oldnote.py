from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.notes.utilities.keyboards import note_chooser
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Command


@vk_bot.message_handler(
    PayloadFilter(payload={ "callback": Command.NOTES_SHOW.value }) |
    PayloadFilter(payload={ "callback": Command.NOTES_DELETE.value })
)
async def choose_note(event: SimpleBotEvent):
    if event.payload["callback"] == Command.NOTES_SHOW.value:
        action: Command = Command.NOTES_SHOW
    elif event.payload["callback"] == Command.NOTES_DELETE.value:
        action: Command = Command.NOTES_DELETE
    
    user: User = User.get(User.vk_id == event.peer_id)
    notes: List[Note] = list(Note.select().where(Note.user == user))
    
    await event.answer(
        message="Выбери заметку:",
        keyboard=note_chooser(notes=notes, action=action)
    )


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.NOTES_SHOW_ALL.value }))
async def show_all(event: SimpleBotEvent):
    user: User = User.get(User.vk_id == event.peer_id)
    notes: List[Note] = list(Note.select().where(Note.user == user))
    
    for note in notes:
        await event.answer(message=remove_markdown(note.text))
    
    await event.answer(
        message="Заметок всего: {current}/{max}".format(
            current=len(notes),
            max=MAX_NOTES_NUMBER
        ),
        keyboard=to_menu()
    )

@vk_bot.message_handler(
    PayloadContainsFilter(key=Command.NOTES_SHOW.value),
    PayloadContainsFilter(key="note_id")
)
async def show_note(event: SimpleBotEvent):
    note: Note = Note.get(Note.note_id == event.payload["note_id"])
    
    await event.answer(
        message=remove_markdown(note.text),
        keyboard=to_menu()
    )


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.NOTES_DELETE_ALL.value }))
async def delete_all(event: SimpleBotEvent):
    await event.answer(
        message="Удалено!",
        keyboard=to_menu()
    )
    
    user: User = User.get(User.vk_id == event.peer_id)
    Note.delete().where(Note.user == user).execute()

@vk_bot.message_handler(
    PayloadContainsFilter(key=Command.NOTES_DELETE.value),
    PayloadContainsFilter(key="note_id")
)
async def delete_note(event: SimpleBotEvent):
    note: Note = Note.get(Note.note_id == event.payload["note_id"])
    
    await event.answer(
        message=(
            "Заметка удалена! В ней было:\n\n"
            f"{note.text}"
        ),
        keyboard=to_menu()
    )
    
    note.delete_instance()
