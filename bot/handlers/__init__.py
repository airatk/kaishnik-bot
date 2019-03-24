from bot import kaishnik

from bot.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.constants import REPLIES_TO_UNKNOWN_MESSAGE

from random import choice

@kaishnik.message_handler(
    content_types=[
        "sticker",
        "photo", "video", "audio", "document",
        "voice", "video_note", "location", "contact"
    ]
)
def unknown_nontext_message(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown"
    )

from bot.handlers import setup
from bot.handlers import schedule
from bot.handlers import score
from bot.handlers import locations
from bot.handlers import others
from bot.handlers import creator

@kaishnik.message_handler(
    func=lambda message:
        message.text[0] == "/"
)
def unknown_command(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_COMMAND),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@kaishnik.message_handler(content_types=["text"])
def unknown_text_message(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown"
    )
