from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and
        message.text is not None and message.text.startswith(BOT_ADDRESSING) and
        not User.get(User.telegram_id == message.chat.id).is_setup
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        not User.get(User.telegram_id == message.chat.id).is_setup
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.UNLOGIN)
async def deny_access_on_message(message: Message):
    await message.answer(text="Первоначальная настройка пройдена не полностью, исправляйся — /login")
    
    guards[message.chat.id].drop()

@dispatcher.callback_query_handler(lambda callback: not User.get(User.telegram_id == callback.message.chat.id).is_setup)
@top_notification
async def deny_access_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await deny_access_on_message(callback.message)
