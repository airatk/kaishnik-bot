from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import states
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: User.select().where(User.telegram_id == message.chat.id).exists(),
    commands=[ Command.CANCEL.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.CANCEL)
async def cancel_on_message(message: Message):
    if guards[message.chat.id].text is None:
        await message.answer(text="Запущенных команд нет. Отправь какую-нибудь☺️")
        return
    
    states[message.chat.id].drop()
    guards[message.chat.id].drop()
    
    await message.answer(text="Отменено!")

@dispatcher.callback_query_handler(
    lambda callback:
        User.select().where(User.telegram_id == callback.message.chat.id).exists() and
        callback.data == Command.CANCEL.value
)
@top_notification
async def cancel_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await cancel_on_message(callback.message)
