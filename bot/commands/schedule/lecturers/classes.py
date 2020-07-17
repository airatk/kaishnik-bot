from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students

from bot.commands.schedule.utilities.keyboards import time_period_chooser
from bot.commands.schedule.utilities.classes import common_day_schedule
from bot.commands.schedule.utilities.classes import common_day_selection
from bot.commands.schedule.utilities.classes import common_week_schedule

from bot.shared.helpers import top_notification
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ClassesOptionType
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ScheduleType.CLASSES.value in callback.data
)
@top_notification
async def lecturer_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Преподавателево расписание занятий на:",
        reply_markup=time_period_chooser(lecturer_id=callback.data.split()[1])
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.DAILY.value in callback.data
)
@top_notification
async def lecturer_day_schedule(callback: CallbackQuery):
    await common_day_schedule(command=Commands.LECTURERS, callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.WEEKDAYS.value in callback.data
)
@top_notification
async def lecturer_day_selection(callback: CallbackQuery):
    await common_day_selection(command=Commands.LECTURERS, callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.WEEKLY.value in callback.data
)
@top_notification
async def lecturer_week_schedule(callback: CallbackQuery):
    await common_week_schedule(command=Commands.LECTURERS, callback=callback)
