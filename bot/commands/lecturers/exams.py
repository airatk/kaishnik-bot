from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError
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
    
    lecturer_id: str = callback.data.split()[1]
    schedule: [str] = get_lecturers_schedule(lecturer_id=lecturer_id, TYPE=ScheduleType.EXAMS)
    
    if schedule is None: message_text: str = ResponseError.NO_RESPONSE.value
    elif len(schedule) == 0: message_text: str = ResponseError.NO_DATA.value
    else: message_text: str = schedule
    
    await callback.message.edit_text(
        text=message_text,
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
