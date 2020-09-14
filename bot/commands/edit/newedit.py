from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot import dispatcher
from bot import students

from bot.commands.edit.utilities.keyboards import skip
from bot.commands.edit.utilities.keyboards import weektype_editor
from bot.commands.edit.utilities.keyboards import weekday_editor
from bot.commands.edit.utilities.keyboards import hour_editor
from bot.commands.edit.utilities.keyboards import time_editor
from bot.commands.edit.utilities.keyboards import buildings_editor
from bot.commands.edit.utilities.keyboards import subject_type_editor

from bot.shared.keyboards import canceler
from bot.shared.helpers import top_notification
from bot.shared.constants import BOT_ADDRESSING
from bot.shared.api.subject import StudentSubject
from bot.shared.calendar.types import WeekParity
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        callback.data == Commands.EDIT_ADD.value
)
@top_notification
async def add_edit(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject = StudentSubject()
    students[callback.message.chat.id].edited_subject.dates = ""
    
    await callback.message.edit_text(
        text="Выбери тип недели:",
        reply_markup=weektype_editor()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_WEEKTYPE.value in callback.data
)
@top_notification
async def add_weekday(callback: CallbackQuery):
    weektype: str = callback.data.split()[1]
    
    if weektype != WeekParity.BOTH.value:
        students[callback.message.chat.id].edited_subject.is_even = weektype == WeekParity.EVEN.value
    
    await callback.message.edit_text(
        text="Выбери день:",
        reply_markup=weekday_editor()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_WEEKDAY.value in callback.data
)
@top_notification
async def add_hours(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.weekday = int(callback.data.split()[1])
    
    await callback.message.edit_text(
        text="Выбери час начала пары:",
        reply_markup=hour_editor()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_HOUR.value in callback.data
)
@top_notification
async def add_time(callback: CallbackQuery):
    hour = int(callback.data.split()[1][:-3])
    
    await callback.message.edit_text(
        text="Выбери время начала пары:",
        reply_markup=time_editor(hour=hour)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_TIME.value in callback.data
)
@top_notification
async def add_building(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.time = callback.data.split()[1]
    
    await callback.message.edit_text(
        text="Выбери учебное здание:",
        reply_markup=buildings_editor()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_BUILDING.value in callback.data
)
@top_notification
async def add_auditorium(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.building = callback.data.split()[1]
    
    guard_message: Message = await callback.message.edit_text(
        text="Отправь номер аудитории (или где там у тебя пара).",
        reply_markup=skip(ACTION=Commands.EDIT_AUDITORIUM)
    )
    
    students[callback.message.chat.id].guard.text = Commands.EDIT_AUDITORIUM.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT_AUDITORIUM.value and
        callback.data == Commands.EDIT_AUDITORIUM.value
)
@top_notification
async def skip_auditorium(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.auditorium = ""
    
    await add_subject_title(callback.message)

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and students[message.chat.id].guard.text == Commands.EDIT_AUDITORIUM.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text == Commands.EDIT_AUDITORIUM.value
)
async def add_subject_title(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    if students[message.chat.id].edited_subject.auditorium != "":
        await students[message.chat.id].guard.message.delete()
        
        students[message.chat.id].edited_subject.auditorium = message.text
    
    guard_message: Message = await message.answer(
        text="Отправь название предмета.",
        reply_markup=canceler()
    )
    
    students[message.chat.id].guard.text = Commands.EDIT_SUBJECT_TITLE.value
    students[message.chat.id].guard.message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and students[message.chat.id].guard.text == Commands.EDIT_SUBJECT_TITLE.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text == Commands.EDIT_SUBJECT_TITLE.value
)
async def add_subject_type(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text.replace(BOT_ADDRESSING, "")
    
    students[message.chat.id].edited_subject.title = " ".join([ message.text, "•" ])
    
    await message.delete()
    await students[message.chat.id].guard.message.edit_text(
        text="Выбери тип предмета:",
        reply_markup=subject_type_editor()
    )
    
    students[message.chat.id].guard.text = Commands.EDIT.value

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_SUBJECT_TYPE.value in callback.data
)
@top_notification
async def add_lecturer(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.type = (callback.data.split()[1], False)
    
    guard_message: Message = await callback.message.edit_text(
        text="Отправь имя преподавателя.",
        reply_markup=skip(ACTION=Commands.EDIT_LECTURER)
    )
    
    students[callback.message.chat.id].guard.text = Commands.EDIT_LECTURER.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT_LECTURER.value and
        callback.data == Commands.EDIT_LECTURER.value
)
@top_notification
async def skip_lecturer(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.lecturer = ""
    
    await add_department(callback.message)

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and students[message.chat.id].guard.text == Commands.EDIT_LECTURER.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text == Commands.EDIT_LECTURER.value
)
async def add_department(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    if students[message.chat.id].edited_subject.lecturer != "":
        await students[message.chat.id].guard.message.delete()
        
        students[message.chat.id].edited_subject.lecturer = message.text
    
    guard_message: Message = await message.answer(
        text="Отправь название кафедры.",
        reply_markup=skip(ACTION=Commands.EDIT_DEPARTMENT)
    )
    
    students[message.chat.id].guard.text = Commands.EDIT_DEPARTMENT.value
    students[message.chat.id].guard.message = guard_message

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT_DEPARTMENT.value and
        callback.data == Commands.EDIT_DEPARTMENT.value
)
@top_notification
async def skip_department(callback: CallbackQuery):
    students[callback.message.chat.id].edited_subject.department = ""
    
    await end_edit(callback.message)

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and students[message.chat.id].guard.text == Commands.EDIT_DEPARTMENT.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text == Commands.EDIT_DEPARTMENT.value
)
async def end_edit(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    if students[message.chat.id].edited_subject.department != "":
        await students[message.chat.id].guard.message.delete()
        
        students[message.chat.id].edited_subject.department = message.text
    
    await message.answer(
        text="".join([
            "Запомнено!",
            students[message.chat.id].edited_subject.get()
        ]),
        parse_mode="markdown"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].edited_subjects.append(students[message.chat.id].edited_subject)
    students[message.chat.id].edited_subject = None
    
    save_data(file=USERS_FILE, data=students)
