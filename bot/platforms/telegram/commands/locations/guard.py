from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Command.LOCATIONS.value
)
async def guard(message: Message):
    await message.delete()
