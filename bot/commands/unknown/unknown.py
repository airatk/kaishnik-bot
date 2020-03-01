from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.commands.unknown.utilities.constants import REPLIES_TO_UNKNOWN_MESSAGE

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(content_types=[
    "sticker", "photo", "video", "audio", "document", "voice", "video_note", "location", "contact"
])
async def unknown_nontext_message(message: Message): await messange.delete()

@dispatcher.message_handler(content_types=[ "text" ])
@metrics.increment(Commands.UNKNOWN)
async def unknown_command(message: Message):
    await message.answer(
        text=choice(REPLIES_TO_UNKNOWN_COMMAND if message.is_command() else REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="markdown",
        disable_web_page_preview=True
    )

@dispatcher.callback_query_handler(lambda callback: True)
@metrics.increment(Commands.UNKNOWN)
@top_notification
async def unknown_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text="Ой-ой-ой!🙆🏼‍♀️")
    except Exception:
        await callback.message.edit_text(text="Ой!🙆🏼‍♀️")
    
    students[callback.message.chat.id].guard.drop()
