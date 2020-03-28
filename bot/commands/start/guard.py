from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students

from bot.shared.commands import Commands


@dispatcher.message_handler(lambda message:
    message.chat.type == ChatType.PRIVATE and
    students[message.chat.id].guard.text == Commands.START.value
)
async def guard(message: Message): await message.delete()
