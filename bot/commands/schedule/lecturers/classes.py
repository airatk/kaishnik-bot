from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import guards
from bot import states

from bot.commands.schedule.utilities.keyboards import time_period_chooser
from bot.commands.schedule.utilities.classes import common_add_chosen_date
from bot.commands.schedule.utilities.classes import common_show_chosen_dates

from bot.utilities.helpers import top_notification
from bot.utilities.types import Commands
from bot.utilities.api.types import ScheduleType


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LECTURERS.value and
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
        guards[callback.message.chat.id].text == Commands.LECTURERS.value and
        Commands.CLASSES_CHOOSE.value in callback.data
)
@top_notification
async def lecturer_add_chosen_date(callback: CallbackQuery):
    await common_add_chosen_date(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LECTURERS.value and
        Commands.CLASSES_SHOW.value in callback.data
)
@top_notification
async def lecturer_show_chosen_dates(callback: CallbackQuery):
    await common_show_chosen_dates(command=Commands.LECTURERS, callback=callback)
