from random import choice

from aiogram.types import CallbackQuery
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.lecturers import get_lecturers_schedule


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LECTURERS.value and
        ScheduleType.EXAMS.value in callback.data
)
@top_notification
async def lecturers_exams(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    
    (schedule, response_error) = get_lecturers_schedule(
        lecturer_id=callback.data.split()[1],
        schedule_type=ScheduleType.EXAMS,
        user=user
    )
    
    await callback.message.edit_text(
        text=response_error.value if schedule is None else schedule,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
    
    guards[callback.message.chat.id].drop()
