from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.message_handler(lambda message: not students[message.chat.id].is_setup)
@metrics.increment(Commands.UNLOGIN)
async def deny_access_on_message(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Первоначальная настройка пройдена не полностью, исправляйся — /login"
    )
    
    students[message.chat.id].guard.drop()

@dispatcher.callback_query_handler(lambda callback: not students[callback.message.chat.id].is_setup)
@top_notification
async def deny_access_on_callback(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    await deny_access_on_message(callback.message)
