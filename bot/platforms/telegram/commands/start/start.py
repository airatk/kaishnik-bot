from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.start.utilities.keyboards import make_login

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.users import Users
from bot.models.settings import Settings

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Guard
from bot.utilities.types import State
from bot.utilities.types import Commands


# Accepting new users on any message...
@dispatcher.message_handler(
    lambda message:
        not Users.select().where(Users.telegram_id == message.chat.id).exists()
)
@increment_command_metrics(command=Commands.START)
async def start_on_message(message: Message):
    user: Users = Users.create(telegram_id=message.chat.id)
    _: Settings = Settings.create(user_id=user.user_id)
    
    guards[message.chat.id] = Guard()
    states[message.chat.id] = State()
    
    guard_message: Message = await message.answer(text="Йоу!")
    await message.answer(
        text="Для начала настрой меня на общение с тобой😏",
        reply_markup=make_login()
    )
    
    guards[message.chat.id].text = Commands.START.value
    guards[message.chat.id].message = guard_message

# ...& on any callback
@dispatcher.callback_query_handler(
    lambda callback:
        not Users.select().where(Users.telegram_id == callback.message.chat.id).exists()
)
@top_notification
async def start_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await start_on_command(callback.message)


# Accepting the old users on the `/start` command
@dispatcher.message_handler(
    lambda message:
        message.text == f"/{Commands.RESTART.value}" and Users.get(Users.telegram_id == message.chat.id).is_setup
)
@increment_command_metrics(command=Commands.RESTART)
async def start_on_command(message: Message):
    guards[message.chat.id].drop()

    await message.answer(text="Бот перезапущен, перенастраиваться не нужно.")
    await message.answer(text="Но если очень хочется, то можно через настройки — /settings😉")
