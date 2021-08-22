from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.others.utilities.keyboards import via_vk_pay
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.constants import DONATE
from bot.utilities.helpers import note_metrics
from bot.utilities.helpers import remove_markdown
from bot.utilities.helpers import get_top_donators
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.text.capitalize() == CommandsOfVK.DONATE.value
)
@note_metrics(platform=Platform.VK, command=Command.DONATE)
async def donate(event: SimpleBotEvent):
    await event.answer(
        message=remove_markdown(DONATE.format(top_donators=get_top_donators())),
        dont_parse_links=True,
        keyboard=via_vk_pay()
    )
