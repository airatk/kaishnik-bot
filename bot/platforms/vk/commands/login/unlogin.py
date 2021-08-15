from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.models.users import Users

from bot.platforms.vk.utilities.keyboards import make_login

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        not Users.get(Users.vk_id == event.object.object.message.peer_id).is_setup
)
@increment_command_metrics(command=Commands.UNLOGIN)
async def deny_access_on_message(event: SimpleBotEvent):
    await event.answer(
        message="Первоначальная настройка пройдена не полностью, исправляйся:",
        keyboard=make_login()
    )
    
    guards[event.peer_id].drop()
