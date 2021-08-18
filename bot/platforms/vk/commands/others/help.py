from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.others.utilities.constants import HELP
from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.text.capitalize() == CommandsOfVK.HELP.value
)
@increment_command_metrics(command=Commands.HELP)
async def help(event: SimpleBotEvent):
    await event.answer(
        message=HELP,
        dont_parse_links=True,
        keyboard=to_menu()
    )
