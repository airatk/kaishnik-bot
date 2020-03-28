from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.start.utilities.keyboards import make_login

from bot.shared.helpers import top_notification
from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


# Accepting old users on `/start` command whole new users on any messsage...
@dispatcher.message_handler(
    lambda message:
        message.text == "/" + Commands.START.value or
        message.chat.id not in students
)
@metrics.increment(Commands.START)
async def start_on_command(message: Message):
    students[message.chat.id] = Student()
    
    save_data(file=USERS_FILE, object=students)
    
    guard_message: Message = await message.answer(text="Йоу!")
    
    await message.answer(
        text="Для начала настрой меня на общение с тобой😏",
        reply_markup=make_login()
    )
    
    students[message.chat.id].guard.text = Commands.START.value
    students[message.chat.id].guard.message = guard_message

# ...& on any callback
@dispatcher.callback_query_handler(lambda callback: callback.message.chat.id not in students)
@top_notification
async def start_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await start_on_command(callback.message)
