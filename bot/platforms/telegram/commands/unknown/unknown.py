from random import choice

from aiogram.types import Message
from aiogram.types import ContentType
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode
from aiogram.utils.exceptions import MessageError
from aiogram.utils.exceptions import MessageCantBeDeleted

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import states
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.constants import BOT_ADDRESSING
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.utilities.constants import REPLIES_TO_UNKNOWN_TEXT_MESSAGE
from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        message.content_type != ContentType.TEXT,
    content_types=[ ContentType.ANY ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.UNKNOWN_NONTEXT_MESSAGE)
async def unknown_nontext_message(message: Message):
    try:
        await message.delete()
    except MessageCantBeDeleted:
        pass

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING[:-1]) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ),
    content_types=[ ContentType.TEXT ]
)
@dispatcher.message_handler(
    lambda message: message.chat.type == ChatType.PRIVATE,
    content_types=[ ContentType.TEXT ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.UNKNOWN_TEXT_MESSAGE)
async def unknown_text_message(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text.replace(BOT_ADDRESSING, "")
    
    if message.chat.type != ChatType.PRIVATE and message.text == BOT_ADDRESSING[:-1]:
        text: str = "Че?"
    elif message.is_command():
        text: str = choice(REPLIES_TO_UNKNOWN_COMMAND)
    else:
        text: str = choice(REPLIES_TO_UNKNOWN_TEXT_MESSAGE)
    
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@dispatcher.callback_query_handler(lambda _: True)
@note_metrics(platform=Platform.TELEGRAM, command=Command.UNKNOWN_CALLBACK)
@top_notification
async def unknown_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text="Ой-ой!🙆🏼‍♀️")
    except MessageError:
        await callback.message.edit_text(text="Ой!🙆🏼‍♀️")
    
    states[callback.message.chat.id].drop()
    guards[callback.message.chat.id].drop()
