from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.constants import BRS
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.BRS.value.capitalize()
)
@increment_command_metrics(command=Commands.BRS)
async def brs(event: SimpleBotEvent):
    await event.answer(
        message=remove_markdown(BRS.replace("балльно-", "Балльно-")),
        keyboard=to_menu()
    )
