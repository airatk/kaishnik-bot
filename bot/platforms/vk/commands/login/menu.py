from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.login.utilities.constants import GUIDE_MESSAGE
from bot.platforms.vk.commands.login.utilities.keyboards import login_way_chooser
from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN.value }))
@increment_command_metrics(command=Commands.LOGIN)
async def login(event: SimpleBotEvent):
    message: str = (
        "Вход по номеру зачётки позволяет просматривать баллы БРС.\n"
        "Студенческий билет и зачётка имеют одинаковый номер😉\n"
        "\n"
        "Выбери желаемый путь настройки:"
    )

    is_user_setup: bool = Users.get(Users.vk_id == event.peer_id).is_setup
    
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

    Users.update(is_setup=True).where(Users.vk_id == event.peer_id).execute()
