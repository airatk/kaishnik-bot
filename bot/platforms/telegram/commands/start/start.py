from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.start.utilities.keyboards import make_login

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User
from bot.models.settings import Settings

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.types import Guard
from bot.utilities.types import State


# Accepting new users on any message...
@dispatcher.message_handler(
    lambda message: not User.select().where(User.telegram_id == message.chat.id).exists()
)
async def start_on_message(message: Message):
    user: User = User.create(telegram_id=message.chat.id)
    Settings.insert(user=user).execute()
    
    guards[message.chat.id] = Guard()
    states[message.chat.id] = State()
    
    guard_message: Message = await message.answer(text="Йоу!")
    await message.answer(
        text="Для начала настрой меня на общение с тобой😏",
        reply_markup=make_login()
    )
    
    guards[message.chat.id].text = Command.START.value
    guards[message.chat.id].message = guard_message

# ...& on any callback
@dispatcher.callback_query_handler(
    lambda callback: not User.select().where(User.telegram_id == callback.message.chat.id).exists()
)
@top_notification
async def start_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await start_on_command(callback.message)


# Accepting the old users on the `/start` command
@dispatcher.message_handler(
    lambda message: 
        message.text == f"/{Command.RESTART.value}" and 
        User.get(User.telegram_id == message.chat.id).is_setup
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.RESTART)
async def start_on_command(message: Message):
    guards[message.chat.id].drop()

    await message.answer(text="Бот перезапущен, перенастраиваться не нужно.")
    await message.answer(text="Но если очень хочется, то можно через настройки — /settings😉")
