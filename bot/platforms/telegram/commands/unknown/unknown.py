from random import choice

from aiogram.types import Message
from aiogram.types import ContentType
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode
from aiogram.utils.exceptions import MessageError

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.constants import REPLIES_TO_UNKNOWN_COMMAND
from bot.utilities.constants import REPLIES_TO_UNKNOWN_TEXT_MESSAGE
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        message.content_type != ContentType.TEXT,
    content_types=[ ContentType.ANY ]
)
@increment_command_metrics(command=Commands.UNKNOWN_NONTEXT_MESSAGE)
async def unknown_nontext_message(message: Message):
    await message.delete()

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
@increment_command_metrics(command=Commands.UNKNOWN_TEXT_MESSAGE)
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

@dispatcher.callback_query_handler(lambda callback: True)
@increment_command_metrics(command=Commands.UNKNOWN_CALLBACK)
@top_notification
async def unknown_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text="Ой-ой!🙆🏼‍♀️")
    except MessageError:
        await callback.message.edit_text(text="Ой!🙆🏼‍♀️")
