from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students
from bot import metrics

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        callback.message.chat.id in students and
        callback.data == Commands.CANCEL.value
)
@metrics.increment(Commands.CANCEL)
@top_notification
async def cancel_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    if students[callback.message.chat.id].guard.text is None:
        await callback.message.answer(text="Запущенных команд нет. Отправь какую-нибудь☺️")
        return
    
    students[callback.message.chat.id].guard.drop()
    
    await callback.message.answer(text="Отменено!")
