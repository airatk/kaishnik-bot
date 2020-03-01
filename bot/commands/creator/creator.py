from aiogram.types import Message

from bot import dispatcher

from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import CONTROL_PANEL

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.CREATOR.value ]
)
async def creator(message: Message):
    await message.answer(
        text=CONTROL_PANEL,
        parse_mode="markdown"
    )
