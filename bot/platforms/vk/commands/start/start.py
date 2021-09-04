from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards
from bot.platforms.vk import states

from bot.platforms.vk.commands.start.utilities.keyboards import make_login
from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.models.user import User
from bot.models.settings import Settings

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.types import Guard
from bot.utilities.types import State


# Accepting new users on any message
@vk_bot.message_handler(
    lambda event: not User.select().where(User.vk_id == event.object.object.message.peer_id).exists()
)
async def start(event: SimpleBotEvent):
    user: User = User.create(vk_id=event.peer_id)
    Settings.insert(user=user).execute()
    
    guards[event.peer_id] = Guard()
    states[event.peer_id] = State()

    await event.answer(message="Йоу!")
    await event.answer(
        message="Для начала настрой меня на общение с тобой😏",
        keyboard=make_login()
    )


# Accepting the old users on the `/start` command
@vk_bot.message_handler(
    lambda event:
        User.get(User.vk_id == event.object.object.message.peer_id).is_setup and
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize() == CommandOfVK.RESTART.value
)
@note_metrics(platform=Platform.VK, command=Command.RESTART)
async def restart(event: SimpleBotEvent):
    await event.answer(message="Бот перезапущен, перенастраиваться не нужно.")
    await event.answer(
        message="Но если очень хочется, то можно через настройки в меню😉",
        keyboard=to_menu()
    )
