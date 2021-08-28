from typing import Dict

from peewee import ModelSelect

from aiogram.types import Message
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.commands.creator.utilities.constants import CREATOR_TELEGRAM_ID
from bot.platforms.telegram.commands.creator.utilities.constants import USERS_STATS

from bot.models.user import User

from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR_TELEGRAM_ID,
    commands=[ Command.USERS.value ]
)
async def users(message: Message):
    users: ModelSelect = User.select()
    
    users_stats_filing: Dict[str, str] = {
        "telegram": users.where(User.telegram_id.is_null(False)).count(),
        "vk": users.where(User.vk_id.is_null(False)).count(),
        "groups": users.where(User.user_id.in_(users.where(User.is_setup)) & User.is_group_chat).count(),
        "compact": users.where(User.user_id.in_(users.where(User.is_setup)) & ~User.is_group_chat & User.bb_login.is_null() & User.bb_password.is_null()).count(),
        "bb": users.where(User.user_id.in_(users.where(User.is_setup)) & User.bb_login.is_null(False) & User.bb_password.is_null(False)).count(),
        "setup": users.where(User.is_setup).count(),
        "unsetup": users.where(~User.is_setup).count(),
        "total": users.count()
    }
    
    await message.answer(
        text=USERS_STATS.format(**users_stats_filing),
        parse_mode=ParseMode.MARKDOWN
    )
