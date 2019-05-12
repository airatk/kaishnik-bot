from bot import kbot
from bot import metrics
from bot import top_notification

from bot.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.constants import REPLIES_TO_UNKNOWN_MESSAGE

from random import choice

@kbot.message_handler(
    content_types=[
        "sticker",
        "photo", "video", "audio", "document",
        "voice", "video_note", "location", "contact"
    ]
)
def unknown(non_text_message): kbot.delete_message(chat_id=non_text_message.chat.id, message_id=non_text_message.message_id)

@kbot.message_handler(func=lambda message: message.text.startswith("/"))
@metrics.increment("unknown")
def unknown(command):
    kbot.send_message(
        chat_id=command.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_COMMAND),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@kbot.message_handler(content_types=["text"])
@metrics.increment("unknown")
def unknown(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown"
    )

@kbot.callback_query_handler(func=lambda callback: True)
@metrics.increment("unknown")
@top_notification
def unknown(callback): kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
