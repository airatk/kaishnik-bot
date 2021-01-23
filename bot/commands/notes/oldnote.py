from typing import List

from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import guards

from bot.commands.notes.utilities.keyboards import note_chooser
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.models.users import Users
from bot.models.notes import Notes

from bot.utilities.helpers import top_notification
from bot.utilities.types import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.NOTES.value and
        callback.data in [ Commands.NOTES_SHOW.value, Commands.NOTES_DELETE.value ]
)
@top_notification
async def choose_note(callback: CallbackQuery):
    if callback.data == Commands.NOTES_SHOW.value:
        action: Commands = Commands.NOTES_SHOW
    elif callback.data == Commands.NOTES_DELETE.value:
        action: Commands = Commands.NOTES_DELETE
    
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    notes: List[Notes] = Notes.select().where(Notes.user_id == user_id)
    
    await callback.message.edit_text(
        text="Выбери заметку:",
        reply_markup=note_chooser(
            notes=notes,
            action=action
        )
    )


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.NOTES.value and
        callback.data == Commands.NOTES_SHOW_ALL.value
)
@top_notification
async def show_all(callback: CallbackQuery):
    await callback.message.delete()
    
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    notes: List[Notes] = Notes.select().where(Notes.user_id == user_id)
    
    for note in notes:
        await callback.message.answer(
            text=note.note,
            parse_mode="markdown"
        )
    
    await callback.message.answer(
        text="Заметок всего: *{current}/{max}*".format(
            current=notes.count(),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode="markdown"
    )
    
    guards[callback.message.chat.id].drop()

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.NOTES.value and
        Commands.NOTES_SHOW.value in callback.data
)
@top_notification
async def show_note(callback: CallbackQuery):
    note_id: int = int(callback.data.split()[1])
    
    await callback.message.edit_text(
        text=Notes.get(Notes.note_id == note_id).note,
        parse_mode="markdown"
    )
    
    guards[callback.message.chat.id].drop()


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.NOTES.value and
        callback.data == Commands.NOTES_DELETE_ALL.value
)
@top_notification
async def delete_all(callback: CallbackQuery):
    await callback.message.edit_text(text="Удалено!")
    
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    Notes.delete().where(Notes.user_id == user_id).execute()
    
    guards[callback.message.chat.id].drop()

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.NOTES.value and
        Commands.NOTES_DELETE.value in callback.data
)
@top_notification
async def delete_note(callback: CallbackQuery):
    note_id: int = int(callback.data.split()[1])
    
    note: Notes = Notes.get(Notes.note_id == note_id)
    
    await callback.message.edit_text(
        text=(
            "Заметка удалена! В ней было:\n\n"
            "{note}".format(note=note.note)
        ),
        parse_mode="markdown"
    )
    
    note.delete_instance()
    
    guards[callback.message.chat.id].drop()
