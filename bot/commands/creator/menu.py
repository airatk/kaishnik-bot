from aiogram.types import Message

from bot import dispatcher

from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import CONTROL_PANEL

from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.CREATOR.value ]
)
async def creator(message: Message):
    await message.answer(
        text=CONTROL_PANEL,
        parse_mode="markdown"
    )
