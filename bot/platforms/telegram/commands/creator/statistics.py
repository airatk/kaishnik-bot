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
    setup_users: ModelSelect = User.select().where(User.is_setup)
    
    users_stats_filing: Dict[str, str] = {
        "telegram": User.select().where(User.telegram_id.is_null(False)).count(),
        "vk": User.select().where(User.vk_id.is_null(False)).count(),
        "groups": User.select().where(User.user_id.in_(setup_users) & User.is_group_chat).count(),
        "compact": User.select().where(User.user_id.in_(setup_users) & ~User.is_group_chat & User.bb_login.is_null() & User.bb_password.is_null()).count(),
        "bb": User.select().where(User.user_id.in_(setup_users) & ~User.is_group_chat & User.bb_login.is_null(False) & User.bb_password.is_null(False)).count(),
        "setup": setup_users.count(),
        "unsetup": User.select().where(~User.is_setup).count(),
        "total": User.select().count()
    }
    
    await message.answer(
        text=USERS_STATS.format(**users_stats_filing),
        parse_mode=ParseMode.MARKDOWN
    )
