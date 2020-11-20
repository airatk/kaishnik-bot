from aiogram.types import CallbackQuery

from bot import students

from bot.commands.schedule.utilities.keyboards import dates_appender

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.lecturers import get_lecturers_schedule
from bot.shared.commands import Commands

from random import choice


async def common_add_chosen_date(callback: CallbackQuery):
    callback_data: [str] = callback.data.split(" ")
    
    raw_date: str = callback_data[2]
    
    if raw_date != "":
        if raw_date in students[callback.message.chat.id].chosen_schedule_dates:
            students[callback.message.chat.id].chosen_schedule_dates.remove(raw_date)
        else:
            students[callback.message.chat.id].chosen_schedule_dates.append(raw_date)
    
    chosen_dates_number: int = len(students[callback.message.chat.id].chosen_schedule_dates)
    
    chosen_word_ending: str = "о"
    day_word: str = "день"
    
    if chosen_dates_number == 1: chosen_word_ending = ""
    elif chosen_dates_number < 5: day_word = "дня"
    else: day_word = "дней"
    
    await callback.message.edit_text(
        text="\n".join([
            "" if chosen_dates_number == 0 else "Выбран{chosen_word_ending} *{chosen_dates_number}* {day_word}.".format(
                chosen_word_ending=chosen_word_ending,
                chosen_dates_number=chosen_dates_number,
                day_word=day_word
            ),
            "Выбери нужные дни:"
        ]),
        parse_mode="markdown",
        reply_markup=dates_appender(shift=int(callback_data[1]), dates=students[callback.message.chat.id].chosen_schedule_dates, lecturer_id=callback_data[3])
    )

async def common_show_chosen_dates(command: Commands, callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data: [str] = callback.data.split(" ")
    
    if callback_data[1] != "":
        students[callback.message.chat.id].chosen_schedule_dates.append(callback_data[1])
    
    if command is Commands.CLASSES:
        (schedule, error_message) = students[callback.message.chat.id].get_schedule(TYPE=ScheduleType.CLASSES)
    elif command is Commands.LECTURERS:
        (schedule, error_message) = get_lecturers_schedule(
            lecturer_id=callback_data[2],
            TYPE=ScheduleType.CLASSES,
            dates=students[callback.message.chat.id].chosen_schedule_dates,
            settings=students[callback.message.chat.id].settings
        )
    
    await callback.message.delete()
    
    if schedule is None:
        await callback.message.answer(text=error_message, parse_mode="markdown", disable_web_page_preview=True)
    else:
        for day in schedule:
            await callback.message.answer(text=day, parse_mode="markdown")
    
    students[callback.message.chat.id].guard.drop()
