from bot import bot
from bot import students
from bot import metrics

from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_MESSAGE

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands

from random import choice


@bot.message_handler(content_types=[ "sticker", "photo", "video", "audio", "document", "voice", "video_note", "location", "contact" ])
def unknown_nontext_message(message): bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@bot.message_handler()
@metrics.increment(Commands.UNKNOWN)
def unknown_command(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_COMMAND if message.text.startswith("/") else REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.callback_query_handler(func=lambda callback: True)
@metrics.increment(Commands.UNKNOWN)
@top_notification
def unknown_callback(callback):
    try:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Ой-ой-ой!🙆🏼‍♀️"
        )
    except Exception:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Ой!🙆🏼‍♀️"
        )
    
    students[callback.message.chat.id].guard.drop()
