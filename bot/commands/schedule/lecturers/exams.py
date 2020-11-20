from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.lecturers import get_lecturers_schedule
from bot.shared.commands import Commands

from random import choice


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ScheduleType.EXAMS.value in callback.data
)
@top_notification
async def lecturers_exams(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (schedule, error_message) = get_lecturers_schedule(
        lecturer_id=callback.data.split()[1],
        TYPE=ScheduleType.EXAMS,
        settings=students[callback.message.chat.id].settings
    )
    
    await callback.message.edit_text(
        text=error_message if schedule is None else schedule,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].guard.drop()
