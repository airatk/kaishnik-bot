from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.keyboards import canceler
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import clarify_markdown
from bot.utilities.types import Command


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.NOTES.value and
        callback.data == Command.NOTES_ADD.value
)
@top_notification
async def add_note_hint(callback: CallbackQuery):
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    note_number: int = Note.select().where(Note.user == user).count() + 1
    
    if note_number > MAX_NOTES_NUMBER:
        await callback.message.edit_text(text="{max}-заметковый лимит уже достигнут.".format(max=MAX_NOTES_NUMBER))
        
        guards[callback.message.chat.id].drop()
        return
    
    guard_message: Message = await callback.message.edit_text(
        text=(
            "Добавляемая заметка будет *{note_number}* по счёту.\n\n"
            "• Используй звёздочки, чтобы выделить \**жирным*\*\n"
            "• Используй нижнее подчёркивание, чтобы выделить \__курсивом_\_\n\n"
            "Напиши заметку и отправь решительно.".format(note_number=note_number)
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Command.NOTES_ADD.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and guards[message.chat.id].text == Command.NOTES_ADD.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Command.NOTES_ADD.value
)
async def add_note(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    Note.insert(
        user=User.get(User.telegram_id == message.chat.id),
        text=clarify_markdown(message.text)
    ).execute()
    
    await guards[message.chat.id].message.edit_text(text="Запомнено!")
    
    guards[message.chat.id].drop()
