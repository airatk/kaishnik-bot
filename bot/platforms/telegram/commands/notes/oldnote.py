from typing import List

from aiogram.types import CallbackQuery
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.notes.utilities.keyboards import note_chooser
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.types import Command


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.NOTES.value and
        callback.data in [ Command.NOTES_SHOW.value, Command.NOTES_DELETE.value ]
)
@top_notification
async def choose_note(callback: CallbackQuery):
    if callback.data == Command.NOTES_SHOW.value:
        action: Command = Command.NOTES_SHOW
    elif callback.data == Command.NOTES_DELETE.value:
        action: Command = Command.NOTES_DELETE
    
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    notes: List[Note] = list(Note.select().where(Note.user == user))
    
    await callback.message.edit_text(
        text="Выбери заметку:",
        reply_markup=note_chooser(
            notes=notes,
            action=action
        )
    )


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.NOTES.value and
        callback.data == Command.NOTES_SHOW_ALL.value
)
@top_notification
async def show_all(callback: CallbackQuery):
    await callback.message.delete()
    
    user: int = User.get(User.telegram_id == callback.message.chat.id).user_id
    notes: List[Note] = list(Note.select().where(Note.user == user))
    
    for note in notes:
        await callback.message.answer(
            text=note.text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    await callback.message.answer(
        text="Заметок всего: *{current}/{max}*".format(
            current=len(notes),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode=ParseMode.MARKDOWN
    )
    
    guards[callback.message.chat.id].drop()

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.NOTES.value and
        Command.NOTES_SHOW.value in callback.data
)
@top_notification
async def show_note(callback: CallbackQuery):
    note_id: int = int(callback.data.split()[1])
    note: Note = Note.get(Note.note_id == note_id)

    await callback.message.edit_text(
        text=note.text,
        parse_mode=ParseMode.MARKDOWN
    )
    
    guards[callback.message.chat.id].drop()


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.NOTES.value and
        callback.data == Command.NOTES_DELETE_ALL.value
)
@top_notification
async def delete_all(callback: CallbackQuery):
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    Note.delete().where(Note.user == user).execute()

    await callback.message.edit_text(text="Удалено!")
    
    guards[callback.message.chat.id].drop()

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.NOTES.value and
        Command.NOTES_DELETE.value in callback.data
)
@top_notification
async def delete_note(callback: CallbackQuery):
    note_id: int = int(callback.data.split()[1])
    
    note: Note = Note.get(Note.note_id == note_id)
    
    await callback.message.edit_text(
        text=(
            "Заметка удалена! В ней было:\n\n"
            f"{note.text}"
        ),
        parse_mode=ParseMode.MARKDOWN
    )
    
    note.delete_instance()
    
    guards[callback.message.chat.id].drop()
