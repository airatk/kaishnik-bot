from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher

from bot import students

from bot.commands.notes.utilities.helpers import clarify_markdown
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.helpers import top_notification
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.NOTES.value and
        callback.data == Commands.NOTES_ADD.value
)
@top_notification
async def add_note_hint(callback: CallbackQuery):
    number: int = len(students[callback.message.chat.id].notes) + 1
    
    if number > MAX_NOTES_NUMBER:
        await callback.message.edit_text(text="{max}-заметковый лимит уже достигнут.".format(max=MAX_NOTES_NUMBER))
        
        students[callback.message.chat.id].guard.drop()
        return
    
    guard_message: Message = await callback.message.edit_text(
        text=(
            "Добавляемая заметка будет *{number}* по счёту.\n\n"
            "• Используй звёздочки, чтобы выделить \**жирным*\*\n"
            "• Используй нижнее подчёркивание, чтобы выделить \__курсивом_\_\n\n"
            "Напиши заметку и отправь решительно.".format(number=number)
        ),
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.text = Commands.NOTES_ADD.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.message_handler(lambda message: students[message.chat.id].guard.text == Commands.NOTES_ADD.value)
async def add_note(message: Message):
    await message.delete()
    await students[message.chat.id].guard.message.edit_text(text="Запомнено!")
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].notes.append(clarify_markdown(message.text))
    
    save_data(file=USERS_FILE, object=students)
