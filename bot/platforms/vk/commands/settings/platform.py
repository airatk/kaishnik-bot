from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.users import Users

from bot.utilities.constants import PLATFORM_CODE_INFO
from bot.utilities.helpers import generate_platform_code
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Commands


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.SETTINGS_PLATFORM_CODE.value }))
async def appearance_done(event: SimpleBotEvent):
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    platform_code: str = generate_platform_code(user_id=user_id)
    
    await event.answer(
        message=remove_markdown(PLATFORM_CODE_INFO.format(platform_code=platform_code)),
        keyboard=to_menu()
    )
