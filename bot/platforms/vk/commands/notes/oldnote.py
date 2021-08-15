from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.notes.utilities.keyboards import note_chooser
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.users import Users
from bot.models.notes import Notes

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Commands


@vk_bot.message_handler(
    PayloadFilter(payload={ "callback": Commands.NOTES_SHOW.value }) |
    PayloadFilter(payload={ "callback": Commands.NOTES_DELETE.value })
)
async def choose_note(event: SimpleBotEvent):
    if event.payload["callback"] == Commands.NOTES_SHOW.value:
        action: Commands = Commands.NOTES_SHOW
    elif event.payload["callback"] == Commands.NOTES_DELETE.value:
        action: Commands = Commands.NOTES_DELETE
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    notes: List[Notes] = Notes.select().where(Notes.user_id == user_id)
    
    await event.answer(
        message="Выбери заметку:",
        keyboard=note_chooser(notes=notes, action=action)
    )


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.NOTES_SHOW_ALL.value }))
async def show_all(event: SimpleBotEvent):
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    notes: List[Notes] = Notes.select().where(Notes.user_id == user_id)
    
    for note in notes:
        await event.answer(
            message=remove_markdown(note.note)
        )
    
    await event.answer(
        message="Заметок всего: {current}/{max}".format(
            current=notes.count(),
            max=MAX_NOTES_NUMBER
        ),
        keyboard=to_menu()
    )

@vk_bot.message_handler(
    PayloadContainsFilter(key=Commands.NOTES_SHOW.value),
    PayloadContainsFilter(key="note_id")
)
async def show_note(event: SimpleBotEvent):
    note_id: int = event.payload["note_id"]
    
    note: Notes = Notes.get(Notes.note_id == note_id)

    await event.answer(
        message=remove_markdown(note.note),
        keyboard=to_menu()
    )


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.NOTES_DELETE_ALL.value }))
async def delete_all(event: SimpleBotEvent):
    await event.answer(
        message="Удалено!",
        keyboard=to_menu()
    )
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    Notes.delete().where(Notes.user_id == user_id).execute()

@vk_bot.message_handler(
    PayloadContainsFilter(key=Commands.NOTES_DELETE.value),
    PayloadContainsFilter(key="note_id")
)
async def delete_note(event: SimpleBotEvent):
    note_id: int = event.payload["note_id"]

    note: Notes = Notes.get(Notes.note_id == note_id)
    
    await event.answer(
        message=(
            "Заметка удалена! В ней было:\n\n"
            "{note}".format(note=remove_markdown(note.note))
        ),
        keyboard=to_menu()
    )
    
    note.delete_instance()
