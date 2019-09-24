from bot import bot
from bot import students

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError
from bot.shared.api.lecturers import get_lecturers_schedule
from bot.shared.commands import Commands

from random import choice


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        ScheduleType.EXAMS.value in callback.data
)
@top_notification
def lecturers_exams(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    lecturer_id = callback.data.split()[1]
    schedule = get_lecturers_schedule(lecturer_id=lecturer_id, TYPE=ScheduleType.EXAMS)
    
    if schedule is None: message_text = ResponseError.NO_RESPONSE.value
    elif schedule == []: message_text = ResponseError.NO_DATA.value
    else: message_text = schedule
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=message_text,
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
