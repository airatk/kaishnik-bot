from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup

from bot import students

from bot.commands.schedule.utilities.keyboards import weektype_chooser
from bot.commands.schedule.utilities.keyboards import weekday_chooser

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError
from bot.shared.api.lecturers import get_lecturers_schedule
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.commands import Commands

from random import choice


async def common_day_schedule(command: Commands, callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (weektype, weekday, lecturer_id) = callback.data.split()[1:]
    schedule: [str] = None
    
    if command is Commands.CLASSES:
        schedule = students[callback.message.chat.id].get_schedule(
            TYPE=ScheduleType.CLASSES,
            weektype=weektype
        )
    elif command is Commands.LECTURERS:
        schedule = get_lecturers_schedule(
            lecturer_id=lecturer_id,
            TYPE=ScheduleType.CLASSES,
            weektype=weektype,
            settings=students[callback.message.chat.id].settings
        )
    
    if schedule is None: message_text: str = ResponseError.NO_RESPONSE.value
    elif len(schedule) == 0: message_text: str = ResponseError.NO_DATA.value
    else: message_text: str = schedule[int(weekday)]
    
    await callback.message.edit_text(
        text=message_text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
    
    if command is Commands.CLASSES and schedule is None and students[callback.message.chat.id].classes_offline != []:
        await callback.message.answer(
            text=students[callback.message.chat.id].classes_offline[int(weekday)],
            parse_mode="markdown"
        )
        
        await callback.message.answer(text="Отображено расписание, сохранённое ранее.")
    
    students[callback.message.chat.id].guard.drop()

async def common_weektype_selection(command: Commands, callback: CallbackQuery):
    lecturer_id = callback.data.split()[1]
    reply_markup: InlineKeyboardMarkup = None
    
    if command is Commands.CLASSES:
        reply_markup = weektype_chooser()
    elif command is Commands.LECTURERS:
        reply_markup = weektype_chooser(lecturer_id=lecturer_id)
    
    await callback.message.edit_text(
        text="Выбери нужную неделю:",
        reply_markup=reply_markup
    )

async def common_day_selection(command: Commands, callback: CallbackQuery):
    (weektype, lecturer_id) = callback.data.split()[1:]
    reply_markup: InlineKeyboardMarkup = None
    
    if command is Commands.CLASSES:
        reply_markup = weekday_chooser(weektype=weektype)
    elif command is Commands.LECTURERS:
        reply_markup = weekday_chooser(
            weektype=weektype,
            lecturer_id=lecturer_id
        )
    
    await callback.message.edit_text(
        text="Выбери нужный день:",
        reply_markup=reply_markup
    )

async def common_week_schedule(command: Commands, callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (weektype, lecturer_id) = callback.data.split()[1:]
    schedule: [str] = None
    
    if command is Commands.CLASSES:
        schedule = students[callback.message.chat.id].get_schedule(
            TYPE=ScheduleType.CLASSES,
            weektype=weektype
        )
    elif command is Commands.LECTURERS:
        schedule = get_lecturers_schedule(
            lecturer_id=lecturer_id,
            TYPE=ScheduleType.CLASSES,
            weektype=weektype,
            settings=students[callback.message.chat.id].settings
        )
    
    if schedule is None:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        if command is Commands.CLASSES and students[callback.message.chat.id].classes_offline != []:
            for weekday in WEEKDAYS:
                await callback.message.answer(
                    text=students[callback.message.chat.id].classes_offline[weekday - 1],
                    parse_mode="markdown"
                )
            
            await callback.message.answer(text="Отображено расписание, сохранённое ранее.")
    elif len(schedule) == 0:
        await callback.message.edit_text(
            text=ResponseError.NO_DATA.value,
            disable_web_page_preview=True
        )
    else:
        await callback.message.delete()
        
        for weekday in WEEKDAYS:
            await callback.message.answer(
                text=schedule[weekday - 1],
                parse_mode="markdown"
            )
    
    students[callback.message.chat.id].guard.drop()
