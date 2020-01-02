from aiogram.types import CallbackQuery

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.lecturers.utilities.keyboards import lecturer_weektype_chooser
from bot.commands.lecturers.utilities.keyboards import lecturer_weekday_chooser

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ClassesOptionType
from bot.shared.api.types import ResponseError
from bot.shared.api.lecturers import get_lecturers_schedule
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekType
from bot.shared.commands import Commands

from datetime import datetime
from random import choice


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ScheduleType.CLASSES.value in callback.data
)
@top_notification
async def lecturers_week_type_classes(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Преподавателево расписание занятий на:",
        reply_markup=lecturer_weektype_chooser(lecturer_id=callback.data.split()[1])
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.DAILY.value in callback.data
)
@top_notification
async def one_day_lecturer_schedule(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (weektype, weekday, lecturer_id) = callback.data.split()[1:]
    
    schedule: [str] = get_lecturers_schedule(
        lecturer_id=lecturer_id,
        TYPE=ScheduleType.CLASSES,
        is_next=weektype == WeekType.NEXT.value
    )
    
    if schedule is None: message_text: str = ResponseError.NO_RESPONSE.value
    elif len(schedule) == 0: message_text: str = ResponseError.NO_DATA.value
    else: message_text: str = schedule[int(weekday)]
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=message_text,
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.WEEKDAYS.value in callback.data
)
@top_notification
async def certain_date_schedule(callback: CallbackQuery):
    (weektype, lecturer_id) = callback.data.split()[1:]
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=lecturer_weekday_chooser(
            is_next=weektype == WeekType.NEXT.value,
            lecturer_id=lecturer_id
        )
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.WEEKLY.value in callback.data
)
@top_notification
async def weekly_lecturer_schedule(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (weektype, lecturer_id) = callback.data.split()[1:]
    
    schedule: [str] = get_lecturers_schedule(
        lecturer_id=lecturer_id,
        TYPE=ScheduleType.CLASSES,
        is_next=weektype == WeekType.NEXT.value
    )
    
    if schedule is None:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value
        )
    elif len(schedule) == 0:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_DATA.value
        )
    else:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        for weekday in WEEKDAYS:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=schedule[weekday - 1],
                parse_mode="markdown"
            )
    
    students[callback.message.chat.id].guard.drop()
