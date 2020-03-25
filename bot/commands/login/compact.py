from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher
from bot import students

from bot.commands.login.menu import finish_login

from bot.shared.keyboards import canceler
from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ResponseError
from bot.shared.api.student import Student
from bot.shared.commands import Commands

from random import choice


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN.value and
        callback.data == Commands.LOGIN_COMPACT.value
)
@top_notification
async def login_compact(callback: CallbackQuery):
    # Resetting user
    students[callback.message.chat.id] = Student()
    
    students[callback.message.chat.id].is_setup = False
    students[callback.message.chat.id].is_full = False
    
    guard_message = await callback.message.edit_text(
        text="Отправь номер своей группы.",
        reply_markup=canceler()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_COMPACT.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.message_handler(lambda message: students[message.chat.id].guard.text == Commands.LOGIN_COMPACT.value)
async def set_group(message: Message):
    await message.delete()
    await students[message.chat.id].guard.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[message.chat.id].group = message.text
    
    if students[message.chat.id].group_schedule_id is None:
        await students[message.chat.id].guard.message.edit_text(
            text=ResponseError.NO_GROUP.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        return
    
    await finish_login(message=message)
