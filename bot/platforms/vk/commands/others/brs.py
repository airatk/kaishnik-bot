from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.constants import BRS
from bot.utilities.helpers import note_metrics
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.text.capitalize() == CommandOfVK.BRS.value.capitalize()
)
@note_metrics(platform=Platform.VK, command=Command.BRS)
async def brs(event: SimpleBotEvent):
    await event.answer(
        message=remove_markdown(BRS.replace("балльно-", "Балльно-")),
        keyboard=to_menu()
    )
