from bot import bot
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import BRS

from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.BRS.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.BRS)
def brs(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=BRS,
        parse_mode="Markdown"
    )
