from random import choice

from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.utilities.keyboards import to_menu

from bot.utilities.constants import REPLIES_TO_UNKNOWN_TEXT_MESSAGE
from bot.utilities.constants import REPLIES_TO_UNKNOWN_NONTEXT_MESSAGE
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        len(event.object.object.message.text) == 0
)
@increment_command_metrics(command=Commands.UNKNOWN_NONTEXT_MESSAGE)
async def unknown_nontext_message(event: SimpleBotEvent):
    await event.answer(
        message=choice(REPLIES_TO_UNKNOWN_NONTEXT_MESSAGE),
        keyboard=to_menu()
    )

@vk_bot.message_handler(
    lambda event:
        event.object.object.message.attachments is None or len(event.object.object.message.attachments) == 0
)
@increment_command_metrics(command=Commands.UNKNOWN_TEXT_MESSAGE)
async def unknown_text_message(event: SimpleBotEvent):
    await event.answer(
        message=choice(REPLIES_TO_UNKNOWN_TEXT_MESSAGE),
        dont_parse_links=True,
        keyboard=to_menu()
    )
