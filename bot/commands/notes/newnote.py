from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot import dispatcher
from bot import guards

from bot.commands.notes.utilities.helpers import clarify_markdown
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.models.users import Users
from bot.models.notes import Notes

from bot.utilities.keyboards import canceler
from bot.utilities.helpers import top_notification
from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.NOTES.value and
        callback.data == Commands.NOTES_ADD.value
)
@top_notification
async def add_note_hint(callback: CallbackQuery):
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    note_number: int = Notes.select().where(Notes.user_id == user_id).count() + 1
    
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
        parse_mode="markdown",
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Commands.NOTES_ADD.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and guards[message.chat.id].text == Commands.NOTES_ADD.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Commands.NOTES_ADD.value
)
async def add_note(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    Notes.create(
        user_id=Users.get(Users.telegram_id == message.chat.id).user_id,
        note=clarify_markdown(message.text)
    )
    
    await guards[message.chat.id].message.edit_text(text="Запомнено!")
    
    guards[message.chat.id].drop()
