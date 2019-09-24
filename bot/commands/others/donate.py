from bot import bot
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import DONATE

from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.DONATE.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.DONATE)
def donate(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=DONATE,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
