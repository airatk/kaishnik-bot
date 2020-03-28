from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import DONATE

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.DONATE.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.DONATE.value ]
)
@metrics.increment(Commands.DONATE)
async def donate(message: Message):
    await message.answer(
        text=DONATE,
        parse_mode="markdown",
        disable_web_page_preview=True
    )