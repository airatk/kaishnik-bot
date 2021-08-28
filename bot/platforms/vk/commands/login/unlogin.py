from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.models.user import User

from bot.platforms.vk.commands.login.utilities.keyboards import login_way_chooser

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event: not User.get(User.vk_id == event.object.object.message.peer_id).is_setup
)
@note_metrics(platform=Platform.VK, command=Command.UNLOGIN)
async def deny_access_on_message(event: SimpleBotEvent):
    await event.answer(
        message="Первоначальная настройка пройдена не полностью, исправляйся:",
        keyboard=login_way_chooser(is_old=User.get(vk_id=event.peer_id).is_setup)
    )
    
    guards[event.peer_id].drop()
