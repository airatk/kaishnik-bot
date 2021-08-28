from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.login.utilities.constants import GUIDE_MESSAGE
from bot.platforms.vk.commands.login.utilities.keyboards import login_way_chooser
from bot.platforms.vk.utilities.helpers import is_group_chat
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.LOGIN.value }))
@note_metrics(platform=Platform.VK, command=Command.LOGIN)
async def login(event: SimpleBotEvent):
    message: str = (
        "Вход через ББ позволяет просматривать баллы БРС.\n"
        "Выбери желаемый путь настройки:"
    )

    is_user_setup: bool = User.get(User.vk_id == event.peer_id).is_setup
    
    # Showing the warning to the old users
    if is_user_setup:
        message = "\n\n".join([ "Данные изменятся, но настройки и заметки будут сохранены.", message ])
    
    await event.answer(
        message=message,
        keyboard=login_way_chooser(is_old=is_user_setup)
    )


async def finish_login(event: SimpleBotEvent):
    await event.answer(message="Запомнено!")
    await event.answer(message=GUIDE_MESSAGE, keyboard=to_menu())
    
    User.update(
        is_setup=True,
        is_group_chat=is_group_chat(peer_id=event.peer_id)
    ).where(
        User.vk_id == event.peer_id
    ).execute()
