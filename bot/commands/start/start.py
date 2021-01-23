from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import guards
from bot import states

from bot.commands.start.utilities.keyboards import make_login

from bot.models.users import Users
from bot.models.settings import Settings

from bot.utilities.helpers import top_notification
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Guard
from bot.utilities.types import State
from bot.utilities.types import Commands


# Accepting old users on `/start` command whole new users on any message...
@dispatcher.message_handler(
    lambda message:
        not Users.select().where(Users.telegram_id == message.chat.id).exists()
)
@increment_command_metrics(command=Commands.START)
async def start_on_command(message: Message):
    user: Users = Users.create(telegram_id=message.chat.id)
    
    user.save()
    
    Settings.create(user_id=user.user_id)
    
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
