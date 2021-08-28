from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.locations.utilities.keyboards import location_type_chooser
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event: 
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize() == CommandOfVK.LOCATIONS.value.capitalize()
)
@note_metrics(platform=Platform.VK, command=Command.LOCATIONS)
async def locations(event: SimpleBotEvent):
    await event.answer(
        message="Аж 4 варианта на выбор:",
        keyboard=location_type_chooser()
    )
