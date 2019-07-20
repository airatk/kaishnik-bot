from bot import kbot
from bot import students
from bot import top_notification

from bot.keyboards.lecturers import lecturer_classes_week_type
from bot.keyboards.lecturers import lecturer_certain_date_chooser

from bot.helpers.lecturers import get_lecturers_schedule
from bot.helpers.datatypes import ScheduleType
from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import LOADING_REPLIES

from datetime import datetime
from random import choice


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        ScheduleType.classes.value in callback.data
)
@top_notification
def lecturers_week_type_classes(callback):
    lecturer_id = callback.data.split()[1]
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Преподавателево расписание занятий на:",
        reply_markup=lecturer_classes_week_type(lecturer_id=lecturer_id)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-weekdays" in callback.data
)
@top_notification
def certain_date_schedule(callback):
    callback_data = callback.data.split()
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=lecturer_certain_date_chooser(
            todays_weekday=datetime.today().isoweekday(),
            type=callback_data[1],
            lecturer_id=callback_data[2]
        )
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-daily" in callback.data
)
@top_notification
def one_day_lecturer_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data = callback.data.split()
    
    schedule = get_lecturers_schedule(
        lecturer_id=callback_data[3],
        type=ScheduleType.classes,
        next="next" in callback_data
    )
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=schedule[int(callback_data[2]) - 1] if len(schedule) != 1 else schedule[0],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-weekly" in callback.data
)
@top_notification
def weekly_lecturer_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data = callback.data.split()
    
    schedule = get_lecturers_schedule(
        lecturer_id=callback_data[2],
        type=ScheduleType.classes,
        next="next" in callback_data
    )
    
    if len(schedule) == 1:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=schedule[0]
        )
    else:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        for weekday in WEEKDAYS:
            kbot.send_message(
                chat_id=callback.message.chat.id,
                text=schedule[weekday - 1],
                parse_mode="Markdown"
            )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
