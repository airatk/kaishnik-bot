from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.login.utilities.keyboards import login_way_chooser
from bot.commands.login.utilities.constants import GUIDE_MESSAGE

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE


@dispatcher.callback_query_handler(
    lambda callback: (
            students[callback.message.chat.id].guard.text == Commands.START.value or
            students[callback.message.chat.id].guard.text == Commands.SETTINGS.value
        ) and callback.data == Commands.LOGIN.value
)
@top_notification
async def login_on_callback(callback: CallbackQuery):
    # Cleanning the chat
    await callback.message.delete()
    if students[callback.message.chat.id].guard.text == Commands.START.value: await students[callback.message.chat.id].guard.message.delete()
    
    await login_on_command(callback.message)

@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.LOGIN.value ]
)
@metrics.increment(Commands.LOGIN)
async def login_on_command(message: Message):
    await message.answer(
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


async def finish_login(message: Message):
    await students[message.chat.id].guard.message.edit_text(text="Запомнено!")
    
    await message.answer(
        text=GUIDE_MESSAGE,
        parse_mode="markdown"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].is_setup = True
    
    save_data(file=USERS_FILE, object=students)
