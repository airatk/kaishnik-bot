from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards
from bot.platforms.vk import states

from bot.platforms.vk.utilities.keyboards import make_login
from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.models.users import Users
from bot.models.settings import Settings

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Guard
from bot.utilities.types import State
from bot.utilities.types import Commands


# Accepting new users on any message
@vk_bot.message_handler(
    lambda event:
        not Users.select().where(Users.vk_id == event.object.object.message.peer_id).exists()
)
@increment_command_metrics(command=Commands.START)
async def start(event: SimpleBotEvent):
    guards[event.peer_id] = Guard()
    states[event.peer_id] = State()
    
    user: Users = Users.create(vk_id=event.peer_id)
    _: Settings = Settings.create(user_id=user.user_id)

    await event.answer(message="Йоу!")
    await event.answer(
        message="Для начала настрой меня на общение с тобой😏",
        keyboard=make_login()
    )


# Accepting the old users on the `/start` command
@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.RESTART.value and 
        Users.get(Users.vk_id == event.object.object.message.peer_id).is_setup
)
@increment_command_metrics(command=Commands.RESTART)
async def restart(event: SimpleBotEvent):
    await event.answer(message="Бот перезапущен, перенастраиваться не нужно.")
    await event.answer(
        message="Но если очень хочется, то можно через настройки в меню😉",
        keyboard=to_menu()
    )
