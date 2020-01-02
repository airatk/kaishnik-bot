from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import HELP

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.HELP.value ]
)
@metrics.increment(Commands.HELP)
async def help(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=HELP,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
