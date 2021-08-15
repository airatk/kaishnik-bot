from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.others.utilities.keyboards import via_vk_pay
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.constants import DONATE
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.DONATE.value
)
@increment_command_metrics(command=Commands.DONATE)
async def donate(event: SimpleBotEvent):
    await event.answer(
        message=remove_markdown(DONATE),
        dont_parse_links=True,
        keyboard=via_vk_pay()
    )
