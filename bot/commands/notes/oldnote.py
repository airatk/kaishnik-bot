from bot import bot
from bot import students

from bot.commands.notes.utilities.keyboards import note_chooser
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.helpers import top_notification
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data in [ Commands.NOTES_SHOW.value, Commands.NOTES_DELETE.value ]
)
@top_notification
def choose_note(callback):
    if callback.data == Commands.NOTES_SHOW.value: ACTION = Commands.NOTES_SHOW
    elif callback.data == Commands.NOTES_DELETE.value: ACTION = Commands.NOTES_DELETE
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери заметку:",
        reply_markup=note_chooser(
            notes=students[callback.message.chat.id].notes,
            ACTION=ACTION
        )
    )


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data == Commands.NOTES_SHOW_ALL.value
)
@top_notification
def show_all(callback):
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    for note in students[callback.message.chat.id].notes:
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=note,
            parse_mode="Markdown"
        )
    
    bot.send_message(
        chat_id=callback.message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[callback.message.chat.id].notes),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        Commands.NOTES_SHOW.value in callback.data
)
@top_notification
def show_note(callback):
    number = int(callback.data.split()[1])
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=students[callback.message.chat.id].notes[number],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data == Commands.NOTES_DELETE_ALL.value
)
@top_notification
def delete_all(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Удалено!"
    )
    
    students[callback.message.chat.id].guard.drop()
    students[callback.message.chat.id].notes = []
    
    save_data(file=USERS_FILE, object=students)

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        Commands.NOTES_DELETE.value in callback.data
)
@top_notification
def delete_note(callback):
    number = int(callback.data.split()[1])
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "Заметка удалена! В ней было:\n\n"
            "{note}".format(note=students[callback.message.chat.id].notes[number])
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
    del students[callback.message.chat.id].notes[number]
    
    save_data(file=USERS_FILE, object=students)
