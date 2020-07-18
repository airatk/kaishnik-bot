from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import DICE

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.DICE.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.DICE.value ]
)
@metrics.increment(Commands.DICE)
async def dice(message: Message):
    await message.answer_dice(emoji=DICE)
