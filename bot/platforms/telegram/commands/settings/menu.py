from typing import Any
from typing import Dict

from aiogram.types import Message
from aiogram.types import Chat
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.settings.utilities.keyboards import action_chooser

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import COMPACT_USER_INFO
from bot.utilities.constants import BB_USER_INFO
from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.SETTINGS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.SETTINGS.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.SETTINGS)
async def settings(message: Message):
    chat: Chat = await message.bot.get_chat(chat_id=message.chat.id)
    
    user: User = User.get(User.telegram_id == message.chat.id)
    account_info: Dict[str, str] = {
        "fullname": chat.full_name,
        "username": "" if chat.username is None else " @{username}".format(username=chat.username),
        "chat_id": message.chat.id if message.chat.type == ChatType.PRIVATE else -(message.chat.id + 1_000_000_000_000),
        "login": user.bb_login,
        "password": user.bb_password,
        "group": user.group,
        "notes_number": Note.select().where(Note.user == user).count()
    }
    user_info: str = COMPACT_USER_INFO if user.bb_login is None or user.bb_password is None else BB_USER_INFO
    
    await message.answer(
        text=user_info.format(**account_info),
        reply_markup=action_chooser()
    )
    
    guards[message.chat.id].text = Command.SETTINGS.value
