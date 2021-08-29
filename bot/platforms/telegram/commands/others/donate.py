from aiogram.types import Message
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.utilities.constants import DONATE
from bot.utilities.helpers import note_metrics
from bot.utilities.helpers import get_top_donators
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.DONATE.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.DONATE.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.DONATE)
async def donate(message: Message):
    await message.answer(
        text=DONATE.format(top_donators=get_top_donators()),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
