from bot import bot
from bot import students

from bot.commands.notes.utilities.helpers import clarify_markdown
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.helpers import top_notification
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data == Commands.NOTES_ADD.value
)
@top_notification
def add_note_hint(callback):
    number = len(students[callback.message.chat.id].notes) + 1
    
    if number > MAX_NOTES_NUMBER:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="{max}-заметковый лимит уже достигнут.".format(max=MAX_NOTES_NUMBER)
        )
        
        students[callback.message.chat.id].guard.drop()
        return
    
    guard_message = bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "Добавляемая заметка будет *{number}* по счёту.\n\n"
            "• Используй звёздочки, чтобы выделить \**жирным*\*\n"
            "• Используй нижнее подчёркивание, чтобы выделить \__курсивом_\_\n\n"
            "Напиши заметку и отправь решительно.".format(number=number)
        ),
        parse_mode="Markdown"
    )

    students[callback.message.chat.id].guard.text = Commands.NOTES_ADD.value
    students[callback.message.chat.id].guard.message = guard_message

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.NOTES_ADD.value)
def add_note(message):
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text="Запомнено!"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].notes.append(clarify_markdown(message.text))
    save_data(file=USERS_FILE, object=students)
