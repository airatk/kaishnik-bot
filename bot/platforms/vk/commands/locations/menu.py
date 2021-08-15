from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.locations.utilities.keyboards import location_type_chooser
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.LOCATIONS.value.capitalize()
)
@increment_command_metrics(command=Commands.LOCATIONS)
async def locations(event: SimpleBotEvent):
    await event.answer(
        message="Аж 4 варианта на выбор:",
        keyboard=location_type_chooser()
    )
