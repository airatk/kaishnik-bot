from typing import Optional

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.login.menu import finish_login
from bot.platforms.telegram.utilities.constants import BOT_ADDRESSING
from bot.platforms.telegram.utilities.helpers import top_notification
from bot.platforms.telegram.utilities.keyboards import canceler

from bot.models.user import User

from bot.utilities.helpers import decode_platform_code
from bot.utilities.types import Command


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.START.value and
        callback.data == Command.LOGIN_PLATFORM.value
)
@top_notification
async def login_platform(callback: CallbackQuery):
    await guards[callback.message.chat.id].message.delete()
    guard_message: Message = await callback.message.edit_text(
        text="Отправь код авторизации. Его можно посмотреть в настройках Каиста в ВК.",
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Command.LOGIN_PLATFORM.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and guards[message.chat.id].text == Command.LOGIN_PLATFORM.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Command.LOGIN_PLATFORM.value
)
async def set_user_id(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    user_id: Optional[int] = decode_platform_code(platform_code=message.text)

    if user_id is None or not User.select().where(User.user_id == user_id).exists():
        await guards[message.chat.id].message.edit_text(
            text="Неверный код. Исправляйся.",
            reply_markup=canceler()
        )
        return
    
    User.delete().where(User.telegram_id == message.chat.id).execute()
    User.update(telegram_id=message.chat.id).where(User.user_id == user_id).execute()
    
    await finish_login(message=message)
