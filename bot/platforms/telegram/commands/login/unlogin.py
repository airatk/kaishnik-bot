from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and
        message.text is not None and message.text.startswith(BOT_ADDRESSING) and
        not Users.get(Users.telegram_id == message.chat.id).is_setup
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        not Users.get(Users.telegram_id == message.chat.id).is_setup
)
@increment_command_metrics(command=Commands.UNLOGIN)
async def deny_access_on_message(message: Message):
    await message.answer(text="Первоначальная настройка пройдена не полностью, исправляйся — /login")
    
    guards[message.chat.id].drop()

@dispatcher.callback_query_handler(lambda callback: not Users.get(Users.telegram_id == callback.message.chat.id).is_setup)
@top_notification
async def deny_access_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await deny_access_on_message(callback.message)
