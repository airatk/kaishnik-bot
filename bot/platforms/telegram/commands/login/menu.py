from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.login.utilities.keyboards import login_way_chooser
from bot.platforms.telegram.commands.login.utilities.constants import GUIDE_MESSAGE

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.callback_query_handler(
    lambda callback: (
        guards[callback.message.chat.id].text == Command.START.value or
        guards[callback.message.chat.id].text == Command.SETTINGS.value
    ) and callback.data == Command.LOGIN.value
)
@top_notification
async def login_on_callback(callback: CallbackQuery):
    # Cleaning the chat
    await callback.message.delete()
    if guards[callback.message.chat.id].text == Command.START.value:
        await guards[callback.message.chat.id].message.delete()
    
    await login_on_command(callback.message)

@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.LOGIN.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.LOGIN.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.LOGIN)
async def login_on_command(message: Message):
    if message.chat.type == ChatType.PRIVATE:
        text: str = (
            "Вход через ББ позволяет просматривать баллы БРС.\n"
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
    
    is_user_setup: bool = User.get(User.telegram_id == message.chat.id).is_setup
    
    # Showing the warning to the old users
    if is_user_setup:
        text = "\n\n".join([ "Данные изменятся, но настройки и заметки будут сохранены.", text ])
    
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=login_way_chooser(is_old=is_user_setup, chat_type=message.chat.type)
    )
    
    guards[message.chat.id].text = Command.LOGIN.value


async def finish_login(message: Message):
    await guards[message.chat.id].message.edit_text(text="Запомнено!")
    
    await message.answer(
        text=GUIDE_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )
    
    guards[message.chat.id].drop()
    
    User.update(
        is_setup=True, 
        is_group_chat=(message.chat.type != ChatType.PRIVATE)
    ).where(
        User.telegram_id == message.chat.id
    ).execute()
