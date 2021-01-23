from random import choice

from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import guards
from bot import states

from bot.models.users import Users

from bot.utilities.helpers import top_notification
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.lecturers import get_lecturers_schedule


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LECTURERS.value and
        ScheduleType.EXAMS.value in callback.data
)
@top_notification
async def lecturers_exams(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    
    (schedule, response_error) = get_lecturers_schedule(
        lecturer_id=callback.data.split()[1],
        schedule_type=ScheduleType.EXAMS,
        user_id=user_id
    )
    
    await callback.message.edit_text(
        text=response_error.value if schedule is None else schedule,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
    
    guards[callback.message.chat.id].drop()
