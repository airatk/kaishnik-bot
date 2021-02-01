from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.others.utilities.constants import HELP

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.HELP.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.HELP.value ]
)
@increment_command_metrics(command=Commands.HELP)
async def help(message: Message):
    await message.answer(
        text=HELP,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
