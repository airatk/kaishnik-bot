from aiogram.types import Message

from bot import dispatcher

from bot import students

from bot.shared.commands import Commands


@dispatcher.message_handler(lambda message: students[message.chat.id].guard.text == Commands.EDIT.value)
async def guard(message: Message): await message.delete()
