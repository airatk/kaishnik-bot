from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import states
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import menu
from bot.platforms.vk.utilities.keyboards import additional_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.MENU.value
)
@increment_command_metrics(command=Commands.MENU)
async def menu_on_command(event: SimpleBotEvent):
    states[event.peer_id].drop()
    guards[event.peer_id].drop()
    
    await event.answer(
        message="Список команд:",
        keyboard=menu()
    )

@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.MORE.value
)
@increment_command_metrics(command=Commands.MORE)
async def more_on_command(event: SimpleBotEvent):
    await event.answer(
        message="Список команд:",
        keyboard=additional_menu()
    )
