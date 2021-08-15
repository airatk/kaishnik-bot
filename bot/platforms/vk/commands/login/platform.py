from typing import Optional

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.login.menu import finish_login
from bot.platforms.vk.utilities.keyboards import canceler

from bot.models.users import Users

from bot.utilities.helpers import decode_platform_code
from bot.utilities.types import Commands


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_PLATFORM.value }))
async def login_compact(event: SimpleBotEvent):
    await event.answer(
        message="Отправь код авторизации. Его можно посмотреть в настройках Каиста в Телеграме.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Commands.LOGIN_PLATFORM.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Commands.LOGIN_PLATFORM.value
)
async def set_group(event: SimpleBotEvent):
    user_id: Optional[int] = decode_platform_code(platform_code=event.text)

    if user_id is None or not Users.select().where(Users.user_id == user_id).exists():
        await event.answer(
            message="Неверный код. Исправляйся.",
            keyboard=canceler()
        )
        return
    
    guards[event.peer_id].drop()
    
    Users.delete().where(Users.vk_id == event.peer_id).execute()
    Users.update(vk_id=event.peer_id).where(Users.user_id == user_id).execute()
    
    await finish_login(event=event)
