from aiogram.types import Message
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.utilities.constants import BRS
from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.BRS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.BRS.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.BRS)
async def brs(message: Message):
    await message.answer(
        text=BRS,
        parse_mode=ParseMode.MARKDOWN
    )
