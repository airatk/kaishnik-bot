from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.schedule.utilities.keyboards import time_period_chooser
from bot.platforms.telegram.commands.schedule.utilities.classes import common_add_chosen_date
from bot.platforms.telegram.commands.schedule.utilities.classes import common_show_chosen_dates

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.types import Command
from bot.utilities.api.types import ScheduleType


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LECTURERS.value and
        ScheduleType.CLASSES.value in callback.data
)
@top_notification
async def lecturer_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Преподавателево расписание занятий на:",
        reply_markup=time_period_chooser(lecturer_id=callback.data.split(" ")[1])
    )
    
    states[callback.message.chat.id].chosen_schedule_dates = []

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LECTURERS.value and
        Command.CLASSES_CHOOSE.value in callback.data
)
@top_notification
async def lecturer_add_chosen_date(callback: CallbackQuery):
    await common_add_chosen_date(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LECTURERS.value and
        Command.CLASSES_SHOW.value in callback.data
)
@top_notification
async def lecturer_show_chosen_dates(callback: CallbackQuery):
    await common_show_chosen_dates(command=Command.LECTURERS, callback=callback)
