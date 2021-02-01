from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.login.utilities.keyboards import login_way_chooser
from bot.platforms.telegram.commands.login.utilities.constants import GUIDE_MESSAGE

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Commands


@dispatcher.callback_query_handler(
    lambda callback: (
        guards[callback.message.chat.id].text == Commands.START.value or
        guards[callback.message.chat.id].text == Commands.SETTINGS.value
    ) and callback.data == Commands.LOGIN.value
)
@top_notification
async def login_on_callback(callback: CallbackQuery):
    # Cleaning the chat
    await callback.message.delete()
    if guards[callback.message.chat.id].text == Commands.START.value:
        await guards[callback.message.chat.id].message.delete()
    
    await login_on_command(callback.message)

@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.LOGIN.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.LOGIN.value ]
)
@increment_command_metrics(command=Commands.LOGIN)
async def login_on_command(message: Message):
    if message.chat.type == ChatType.PRIVATE:
        text: str = (
            "Студенческий билет и зачётка имеют одинаковый номер😉\n"
            "\n"
            "Выбери желаемый путь настройки:"
        )
    else:
        text: str = (
            "Текстовые сообщения должны начинаться с обращения {bot_addressing} либо быть реплаями, команды — не должны:\n"
            "\n"
            "• /command\n"
            "• {bot_addressing} текст\n"
            "• текст (в случае, если реплай)"
        ).format(bot_addressing=BOT_ADDRESSING[:-1])
    
    is_user_setup: bool = Users.get(Users.telegram_id == message.chat.id).is_setup
    
    # Showing the warning to the old users
    if is_user_setup:
        text = "\n\n".join([ "Данные изменятся, но настройки и заметки будут сохранены.", text ])
    
    await message.answer(
        text=text,
        parse_mode="markdown",
        reply_markup=login_way_chooser(is_old=is_user_setup, chat_type=message.chat.type)
    )
    
    guards[message.chat.id].text = Commands.LOGIN.value


async def finish_login(message: Message):
    await guards[message.chat.id].message.edit_text(text="Запомнено!")
    
    await message.answer(
        text=GUIDE_MESSAGE,
        parse_mode="markdown"
    )
    
    guards[message.chat.id].drop()
    
    Users.update(is_setup=True).where(Users.telegram_id == message.chat.id).execute()
