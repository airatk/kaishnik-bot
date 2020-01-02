from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.login.utilities.constants import GUIDE_MESSAGE

from bot.shared.keyboards import cancel_option
from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ResponseError
from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
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
    
    guard_message = await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер своей группы.",
        reply_markup=cancel_option()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_COMPACT.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.message_handler(lambda message: students[message.chat.id].guard.text == Commands.LOGIN_COMPACT.value)
async def set_group(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[message.chat.id].group = message.text
    
    if students[message.chat.id].group_schedule_id is None:
        await bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text=ResponseError.NO_GROUP.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        return
    
    await bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text="Запомнено!"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=GUIDE_MESSAGE,
        parse_mode="markdown"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].is_setup = True
    
    save_data(file=USERS_FILE, object=students)
