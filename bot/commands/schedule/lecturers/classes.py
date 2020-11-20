from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students

from bot.commands.schedule.utilities.keyboards import time_period_chooser
from bot.commands.schedule.utilities.classes import common_add_chosen_date
from bot.commands.schedule.utilities.classes import common_show_chosen_dates

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
    students[callback.message.chat.id].chosen_schedule_dates = []
    
    await callback.message.edit_text(
        text="Преподавателево расписание занятий на:",
        reply_markup=time_period_chooser(lecturer_id=callback.data.split(" ")[1])
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.CHOOSE.value in callback.data
)
@top_notification
async def lecturer_add_chosen_date(callback: CallbackQuery):
    await common_add_chosen_date(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ClassesOptionType.SHOW.value in callback.data
)
@top_notification
async def lecturer_show_chosen_dates(callback: CallbackQuery):
    await common_show_chosen_dates(command=Commands.LECTURERS, callback=callback)
