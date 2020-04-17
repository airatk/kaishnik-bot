from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.login.utilities.keyboards import login_way_chooser
from bot.commands.login.utilities.constants import GUIDE_MESSAGE

from bot.shared.helpers import top_notification
from bot.shared.constants import BOT_ADDRESSING
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
    # Cleaning the chat
    await callback.message.delete()
    if students[callback.message.chat.id].guard.text == Commands.START.value: await students[callback.message.chat.id].guard.message.delete()
    
    await login_on_command(callback.message)

@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.LOGIN.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.LOGIN.value ]
)
@metrics.increment(Commands.LOGIN)
async def login_on_command(message: Message):
    if message.chat.type == ChatType.PRIVATE:
        text: str = (
            "Студенческий билет и зачётка имеют одинаковый номер😉\n"
            "\n"
            "Выбери желаемый путь настройки:"
        )
    else:
        text: str = (
            "Текстовые сообщения должны начинаться с обращения {bot_addressing}, команды — не должны:\n"
            "\n"
            "• /command\n"
            "• {bot_addressing} текст"
        ).format(bot_addressing=BOT_ADDRESSING[:-1])
    
    # Showing the warning to the old users
    if students[message.chat.id].is_setup:
        text = "\n\n".join([ "Все текущие данные, включая *заметки* и *изменённое расписание*, будут стёрты.", text ])
    
    await message.answer(
        text=text,
        parse_mode="markdown",
        reply_markup=login_way_chooser(is_old=students[message.chat.id].is_setup, chat_type=message.chat.type)
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
