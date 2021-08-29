from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import states
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event:
        User.select().where(User.vk_id == event.object.object.message.peer_id).exists() and
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize() == CommandOfVK.CANCEL.value
)
@vk_bot.message_handler(
    lambda event: User.select().where(User.vk_id == event.object.object.message.peer_id).exists(),
    PayloadFilter(payload={ "callback": Command.CANCEL.value })
)
@note_metrics(platform=Platform.VK, command=Command.CANCEL)
async def cancel(event: SimpleBotEvent):
    states[event.peer_id].drop()
    guards[event.peer_id].drop()
    
    await event.answer(
        message="Отменено!",
        keyboard=to_menu()
    )
