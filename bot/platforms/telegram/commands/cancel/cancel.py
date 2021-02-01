from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: Users.select().where(Users.telegram_id == message.chat.id).exists(),
    commands=[ Commands.CANCEL.value ]
)
@increment_command_metrics(command=Commands.CANCEL)
async def cancel_on_message(message: Message):
    if guards[message.chat.id].text is None:
        await message.answer(text="Запущенных команд нет. Отправь какую-нибудь☺️")
        return
    
    guards[message.chat.id].drop()
    
    await message.answer(text="Отменено!")

@dispatcher.callback_query_handler(
    lambda callback:
        Users.select().where(Users.telegram_id == callback.message.chat.id).exists() and
        callback.data == Commands.CANCEL.value
)
@top_notification
async def cancel_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await cancel_on_message(callback.message)
