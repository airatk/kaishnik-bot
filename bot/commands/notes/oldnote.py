from aiogram.types import CallbackQuery

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.notes.utilities.keyboards import note_chooser
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.helpers import top_notification
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data in [ Commands.NOTES_SHOW.value, Commands.NOTES_DELETE.value ]
)
@top_notification
async def choose_note(callback: CallbackQuery):
    if callback.data == Commands.NOTES_SHOW.value: ACTION: Commands = Commands.NOTES_SHOW
    elif callback.data == Commands.NOTES_DELETE.value: ACTION: Commands = Commands.NOTES_DELETE
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери заметку:",
        reply_markup=note_chooser(
            notes=students[callback.message.chat.id].notes,
            ACTION=ACTION
        )
    )


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data == Commands.NOTES_SHOW_ALL.value
)
@top_notification
async def show_all(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    for note in students[callback.message.chat.id].notes:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=note,
            parse_mode="markdown"
        )
    
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[callback.message.chat.id].notes),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        Commands.NOTES_SHOW.value in callback.data
)
@top_notification
async def show_note(callback: CallbackQuery):
    number: int = int(callback.data.split()[1])
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=students[callback.message.chat.id].notes[number],
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data == Commands.NOTES_DELETE_ALL.value
)
@top_notification
async def delete_all(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Удалено!"
    )
    
    students[callback.message.chat.id].guard.drop()
    students[callback.message.chat.id].notes = []
    
    save_data(file=USERS_FILE, object=students)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        Commands.NOTES_DELETE.value in callback.data
)
@top_notification
async def delete_note(callback: CallbackQuery):
    number: int = int(callback.data.split()[1])
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "Заметка удалена! В ней было:\n\n"
            "{note}".format(note=students[callback.message.chat.id].notes[number])
        ),
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
    del students[callback.message.chat.id].notes[number]
    
    save_data(file=USERS_FILE, object=students)
