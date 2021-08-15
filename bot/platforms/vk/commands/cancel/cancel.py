from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import states
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        Users.select().where(Users.vk_id == event.object.object.message.peer_id).exists() and
        event.object.object.message.text.capitalize() == CommandsOfVK.CANCEL.value
)
@vk_bot.message_handler(
    lambda event:
        Users.select().where(Users.vk_id == event.object.object.message.peer_id).exists(),
    PayloadFilter(payload={ "callback": Commands.CANCEL.value })
)
@increment_command_metrics(command=Commands.CANCEL)
async def cancel(event: SimpleBotEvent):
    states[event.peer_id].drop()
    guards[event.peer_id].drop()
    
    await event.answer(
        message="Отменено!",
        keyboard=to_menu()
    )
