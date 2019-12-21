from telebot.types import Message

from bot import bot

from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import CONTROL_PANEL

from bot.shared.commands import Commands


@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.CREATOR.value ]
)
def creator(message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=CONTROL_PANEL,
        parse_mode="Markdown"
    )
