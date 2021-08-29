from aiogram.types import Message
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.commands.creator.utilities.constants import CREATOR_TELEGRAM_ID
from bot.platforms.telegram.commands.creator.utilities.constants import CONTROL_PANEL

from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR_TELEGRAM_ID,
    commands=[ Command.CREATOR.value ]
)
async def creator(message: Message):
    await message.answer(
        text=CONTROL_PANEL,
        parse_mode=ParseMode.MARKDOWN
    )
