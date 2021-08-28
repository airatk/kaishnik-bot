from random import choice

from typing import List

from aiogram.types import CallbackQuery
from aiogram.types import ParseMode
from aiogram.utils.exceptions import MessageNotModified

from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.schedule.utilities.keyboards import dates_appender

from bot.models.user import User

from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ResponseError
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.student import get_schedule_by_group_schedule_id
from bot.utilities.api.lecturers import get_lecturers_schedule


async def common_add_chosen_date(callback: CallbackQuery):
    # Whitespace is explicitly set as a delimiter to preserve number of received arguments
    callback_data: List[str] = callback.data.split(" ")
    raw_date: str = callback_data[2]
    
    if raw_date != "":
        if raw_date in states[callback.message.chat.id].chosen_schedule_dates:
            states[callback.message.chat.id].chosen_schedule_dates.remove(raw_date)
        else:
            states[callback.message.chat.id].chosen_schedule_dates.append(raw_date)
    
    chosen_dates_number: int = len(states[callback.message.chat.id].chosen_schedule_dates)
    
    chosen_word_ending: str = "о"
    day_word: str = "день"
    
    if chosen_dates_number == 1:
        chosen_word_ending = ""
    elif chosen_dates_number < 5:
        day_word = "дня"
    else:
        day_word = "дней"
    
    try:
        await callback.message.edit_text(
            text="\n".join([
                "" if chosen_dates_number == 0 else f"Выбран{chosen_word_ending} *{chosen_dates_number}* {day_word}.",
                "Выбери нужные дни:"
            ]),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=dates_appender(
                shift=int(callback_data[1]),
                dates=states[callback.message.chat.id].chosen_schedule_dates,
                lecturer_id=callback_data[3]
            )
        )
    except MessageNotModified:
        pass

async def common_show_chosen_dates(command: Command, callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data: List[str] = callback.data.split(" ")
    
    if callback_data[1] != "":
        states[callback.message.chat.id].chosen_schedule_dates.append(callback_data[1])
    
    user_id: int = User.get(User.telegram_id == callback.message.chat.id).user_id
    
    if command is Command.CLASSES:
        (schedule, response_error) = get_schedule_by_group_schedule_id(
            schedule_type=ScheduleType.CLASSES,
            user_id=user_id,
            another_group_schedule_id=states[callback.message.chat.id].another_group_schedule_id,
            dates=states[callback.message.chat.id].chosen_schedule_dates
        )
    elif command is Command.LECTURERS:
        (schedule, response_error) = get_lecturers_schedule(
            lecturer_id=callback_data[2],
            schedule_type=ScheduleType.CLASSES,
            user_id=user_id,
            dates=states[callback.message.chat.id].chosen_schedule_dates,
        )
    else:
        (schedule, response_error) = (None, ResponseError.INCORRECT_SCHEDULE_TYPE)
    
    await callback.message.delete()
    
    if response_error is not None:
        await callback.message.answer(
            text=response_error.value,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    
    if schedule is not None:
        for day in schedule:
            await callback.message.answer(
                text=day,
                parse_mode=ParseMode.MARKDOWN
            )
    
    states[callback.message.chat.id].drop()
    guards[callback.message.chat.id].drop()
