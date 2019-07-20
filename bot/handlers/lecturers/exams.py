from bot import kbot
from bot import students
from bot import top_notification

from bot.helpers.lecturers import get_lecturers_schedule
from bot.helpers.datatypes import ScheduleType
from bot.helpers.constants import LOADING_REPLIES

from random import choice


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        ScheduleType.exams.value in callback.data
)
@top_notification
def send_lecturers_exams(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    lecturer_id = callback.data.split()[1]
    schedule = get_lecturers_schedule(lecturer_id=lecturer_id, type=ScheduleType.exams)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=schedule[0],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None
