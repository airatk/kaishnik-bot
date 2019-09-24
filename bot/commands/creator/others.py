from bot import bot
from bot import students

from bot.commands.creator.utilities.helpers import parse_creator_request
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import BROADCAST_MESSAGE_TEMPLATE
from bot.commands.creator.utilities.types import ReverseOption

from bot.shared.data.helpers import save_data
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import IS_WEEK_REVERSED_FILE
from bot.shared.commands import Commands


@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.BROADCAST.value ]
)
def broadcast(message):
    if message.text == "/broadcast":
        bot.send_message(
            chat_id=message.chat.id,
            text="No broadcast message was found! It's supposed to be right after the */broadcast* command.",
            parse_mode="Markdown"
        )
        return

    broadcast_message = message.text[11:]  # Getting rid of /boardcast command
    
    for chat_id in students:
        try:
            bot.send_message(
                chat_id=chat_id,
                text=BROADCAST_MESSAGE_TEMPLATE.format(broadcast_message=broadcast_message),
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception:
            bot.send_message(
                chat_id=message.chat.id,
                text="{} is inactive! /clear?".format(chat_id)
            )

    bot.send_message(
        chat_id=message.chat.id,
        text="Done! Sent to each & every user."
    )

@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.REVERSE.value ]
)
def reverse(message):
    (option, _) = parse_creator_request(message.text)
    
    if option == ReverseOption.WEEK.value:
        save_data(file=IS_WEEK_REVERSED_FILE, object=not load_from(file=IS_WEEK_REVERSED_FILE))
        
        bot.send_message(
            chat_id=message.chat.id,
            text="Week was #reversed!"
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to reverse type of a week, type */reverse week*",
            parse_mode="Markdown"
        )
