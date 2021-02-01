from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.others.utilities.constants import DONATE

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.DONATE.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.DONATE.value ]
)
@increment_command_metrics(command=Commands.DONATE)
async def donate(message: Message):
    await message.answer(
        text=DONATE,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
