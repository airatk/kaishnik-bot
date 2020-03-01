from aiogram.types import Message

from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import BRS

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.BRS.value ]
)
@metrics.increment(Commands.BRS)
async def brs(message: Message):
    await message.answer(
        text=BRS,
        parse_mode="markdown"
    )
