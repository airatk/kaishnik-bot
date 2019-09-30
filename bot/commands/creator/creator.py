from bot import bot
from bot import keys

from bot.commands.creator.utilities.constants import CONTROL_PANEL

from bot.shared.commands import Commands


@bot.message_handler(
    func=lambda message: message.chat.id == keys.CREATOR,
    commands=[ Commands.CREATOR.value ]
)
def creator(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=CONTROL_PANEL,
        parse_mode="Markdown"
    )
