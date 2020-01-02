from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_MESSAGE

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(content_types=[ "sticker", "photo", "video", "audio", "document", "voice", "video_note", "location", "contact" ])
async def unknown_nontext_message(message: Message): await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dispatcher.message_handler(content_types=[ "text" ])
@metrics.increment(Commands.UNKNOWN)
async def unknown_command(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=choice(REPLIES_TO_UNKNOWN_COMMAND if message.text.startswith("/") else REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="markdown",
        disable_web_page_preview=True
    )

@dispatcher.callback_query_handler(lambda callback: True)
@metrics.increment(Commands.UNKNOWN)
@top_notification
async def unknown_callback(callback: CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Ой-ой-ой!🙆🏼‍♀️"
        )
    except Exception:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Ой!🙆🏼‍♀️"
        )
    
    students[callback.message.chat.id].guard.drop()
