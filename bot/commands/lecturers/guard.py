from telebot.types import Message

from bot import bot
from bot import students

from bot.shared.commands import Commands


@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.LECTURERS.value)
def guard(message: Message): bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
