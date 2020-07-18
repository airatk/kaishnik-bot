from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.schedule.lecturers.utilities.keyboards import lecturer_chooser
from bot.commands.schedule.lecturers.utilities.keyboards import lecturer_info_type_chooser
from bot.commands.schedule.lecturers.utilities.constants import MAX_LECTURERS_NUMBER

from bot.shared.keyboards import canceler
from bot.shared.helpers import top_notification
from bot.shared.constants import BOT_ADDRESSING
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ResponseError
from bot.shared.api.lecturers import get_lecturers_names
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.LECTURERS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.LECTURERS.value ]
)
@metrics.increment(Commands.LECTURERS)
async def lecturers(message: Message):
    guard_message: Message = await message.answer(text=choice(LOADING_REPLIES))
    
    students[message.chat.id].lecturers_names = get_lecturers_names()
    
    if students[message.chat.id].lecturers_names is None:
        await guard_message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id].guard.drop()
        return
    
    await guard_message.edit_text(
        text="Отправь фамилию или ФИО преподавателя.",
        reply_markup=canceler()
    )
    
    students[message.chat.id].guard.text = Commands.LECTURERS_NAME.value
    students[message.chat.id].guard.message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and
        message.text is not None and message.text.startswith(BOT_ADDRESSING) and
        students[message.chat.id].guard.text == Commands.LECTURERS_NAME.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text == Commands.LECTURERS_NAME.value
)
async def find_lecturer(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text[len(BOT_ADDRESSING):]
    
    await message.delete()
    
    name_part: str = message.text.lower()
    names: [{str: str}] = [ name for name in students[message.chat.id].lecturers_names if name_part in name["lecturer"].lower() ]
    
    if len(names) == 0:
        await students[message.chat.id].guard.message.edit_text(text="Ничего не найдено :(")
        
        students[message.chat.id].guard.drop()
        return
    
    if len(names) > MAX_LECTURERS_NUMBER:
        await students[message.chat.id].guard.message.edit_text(text="Слишком мало букв, слишком много преподавателей…")
        
        students[message.chat.id].guard.drop()
        return
    
    await students[message.chat.id].guard.message.edit_text(
        text="Выбери преподавателя:",
        reply_markup=lecturer_chooser(names=names)
    )
    
    students[message.chat.id].guard.text = Commands.LECTURERS.value

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        Commands.LECTURERS.value in callback.data
)
@top_notification
async def lecturers_schedule_type(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Тебе нужны преподавателевы:",
        reply_markup=lecturer_info_type_chooser(lecturer_id=callback.data.split()[1])
    )
