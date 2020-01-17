from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.login.utilities.keyboards import login_way_chooser

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message:
        students[message.chat.id].guard.text == Commands.START.value or
        students[message.chat.id].guard.text is None,
    commands=[ Commands.LOGIN.value ]
)
@metrics.increment(Commands.LOGIN)
async def login_on_command(message: Message):
    guard_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text=(
            "{warning}"
            "Студенческий билет и зачётка имеют одинаковый номер😉\n\n"
            "Выбери желаемый путь настройки:"
        ).format(
            # Showing the warning to the old users
            warning="Все текущие данные, включая *заметки* и *изменённое расписание*, будут стёрты.\n\n" if students[message.chat.id].is_setup else ""
        ),
        parse_mode="markdown",
        reply_markup=login_way_chooser(is_old=students[message.chat.id].is_setup)
    )
    
    students[message.chat.id].guard.text = Commands.LOGIN.value

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.START.value and
        callback.data == Commands.LOGIN.value
)
@metrics.increment(Commands.LOGIN)
@top_notification
async def login_on_callback(callback: CallbackQuery):
    # Cleanning the chat
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.delete_message(chat_id=students[callback.message.chat.id].guard.message.chat.id, message_id=students[callback.message.chat.id].guard.message.message_id)
    
    await login_on_command(callback.message)
