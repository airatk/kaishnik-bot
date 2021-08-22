from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import states
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import menu
from bot.platforms.vk.utilities.keyboards import additional_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.text.capitalize() == CommandOfVK.MENU.value
)
@note_metrics(platform=Platform.VK, command=Command.MENU)
async def menu_on_command(event: SimpleBotEvent):
    states[event.peer_id].drop()
    guards[event.peer_id].drop()
    
    await event.answer(
        message="Список команд:",
        keyboard=menu()
    )

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.text.capitalize() == CommandOfVK.MORE.value
)
@note_metrics(platform=Platform.VK, command=Command.MORE)
async def more_on_command(event: SimpleBotEvent):
    await event.answer(
        message="Список команд:",
        keyboard=additional_menu()
    )
