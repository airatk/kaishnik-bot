from typing import Any
from typing import Dict

from vkwave.bots import SimpleBotEvent
from vkwave.types.responses import UsersGetResponse
from vkwave.types.objects import UsersUserXtrCounters

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.settings.utilities.keyboards import action_chooser
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import COMPACT_USER_INFO
from bot.utilities.constants import BB_USER_INFO
from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize() == CommandOfVK.SETTINGS.value
)
@note_metrics(platform=Platform.VK, command=Command.SETTINGS)
async def settings(event: SimpleBotEvent):
    vk_response: UsersGetResponse = await event.api_ctx.users.get(user_ids=[ event.peer_id ])
    vk_user: UsersUserXtrCounters = vk_response.response[0]
    
    user: User = User.get(User.vk_id == event.peer_id)

    account_info: Dict[str, str] = {
        "fullname": " ".join([ vk_user.first_name, vk_user.last_name ]),
        "username": f" @id{event.peer_id}" if vk_user.nickname is None else f" @{vk_user.nickname}",
        "chat_id": event.peer_id,
        "login": user.bb_login,
        "password": user.bb_password,
        "group": user.group,
        "notes_number": Note.select().where(Note.user == user).count()
    }
    user_info: str = COMPACT_USER_INFO if user.bb_login is None or user.bb_password is None else BB_USER_INFO

    await event.answer(
        message=user_info.format(**account_info),
        keyboard=action_chooser()
    )
