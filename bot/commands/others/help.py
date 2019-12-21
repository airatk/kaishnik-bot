from telebot.types import Message

from bot import bot
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import HELP

from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.HELP.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.HELP)
def help(message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=HELP,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
