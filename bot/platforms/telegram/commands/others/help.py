from aiogram.types import Message
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.others.utilities.constants import HELP

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.HELP.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.HELP.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.HELP)
async def help(message: Message):
    await message.answer(
        text=HELP,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
