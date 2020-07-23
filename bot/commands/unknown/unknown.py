from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.utils.exceptions import MessageError

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_MESSAGE

from bot.shared.helpers import top_notification
from bot.shared.constants import BOT_ADDRESSING
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: message.chat.type == ChatType.PRIVATE,
    content_types=[
        "sticker", "photo", "video", "audio", "document", "voice", "video_note", "location", "contact"
    ]
)
@metrics.increment(Commands.UNKNOWN_NONTEXT_MESSAGE)
async def unknown_nontext_message(message: Message): await message.delete()

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ),
    content_types=[ "text" ]
)
@dispatcher.message_handler(
    lambda message: message.chat.type == ChatType.PRIVATE,
    content_types=[ "text" ]
)
@metrics.increment(Commands.UNKNOWN_TEXT_MESSAGE)
async def unknown_text_message(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text.replace(BOT_ADDRESSING, "")
    
    if message.chat.type != ChatType.PRIVATE and message.text == "": text: str = "Че?"
    else: text: str = choice(REPLIES_TO_UNKNOWN_COMMAND if message.is_command() else REPLIES_TO_UNKNOWN_MESSAGE)
    
    await message.answer(
        text=text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )

@dispatcher.callback_query_handler(lambda callback: True)
@metrics.increment(Commands.UNKNOWN_CALLBACK)
@top_notification
async def unknown_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text="Ой-ой!🙆🏼‍♀️")
    except MessageError:
        await callback.message.edit_text(text="Ой!🙆🏼‍♀️")
    
    students[callback.message.chat.id].guard.drop()
