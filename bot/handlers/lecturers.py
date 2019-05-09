from bot import kbot
from bot import students
from bot import metrics
from bot import hide_loading_notification

from bot.constants import WEEKDAYS

from bot.keyboards.lecturers import choose_lecturer
from bot.keyboards.lecturers import lecturer_schedule_type
from bot.keyboards.lecturers import lecturer_classes_week_type
from bot.keyboards.lecturers import lecturer_certain_date_chooser

from bot.helpers import get_lecturers_names
from bot.helpers import get_lecturers_schedule

from datetime import datetime


@kbot.message_handler(
    commands=["lecturers"],
    func=lambda message: students[message.chat.id].previous_message is None
)
def lecturers(message):
    metrics.increment("lecturers")
    
    students[message.chat.id].previous_message = "/lecturers name"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Введи ФИО преподавателя полностью или частично."
    )

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/lecturers name")
def find_lecturer(message):
    names = get_lecturers_names(message.text)
    
    # Cleanning the chat
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    
    if names is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    
        students[message.chat.id].previous_message = None  # Gate System (GS)
    elif names == []:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Ничего не найдено :("
        )

        students[message.chat.id].previous_message = None  # Gate System (GS)
    else:
        try:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Выбери преподавателя:",
                reply_markup=choose_lecturer(names)
            )
        
            students[message.chat.id].previous_message = "/lecturers"  # Gate System (GS)
        except Exception:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Слишком мало букв, слишком много преподавателей…"
            )

            students[message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "lecturer" in callback.data
)
def lecturers_schedule_type(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужно преподавателево расписание:",
        reply_markup=lecturer_schedule_type(callback.data.replace("lecturer ", ""))
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-classes" in callback.data
)
def lecturers_week_type_classes(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Преподавателево расписание занятий на:",
        reply_markup=lecturer_classes_week_type(callback.data.replace("l-classes ", ""))
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-weekdays" in callback.data
)
def certain_date_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=lecturer_certain_date_chooser(
            todays_weekday=datetime.today().isoweekday(),
            type=callback.data.replace("l-weekdays ", "")[:4],
            prepod_login=callback.data[16:]
        )
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-daily" in callback.data
)
def one_day_lecturer_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=get_lecturers_schedule(
            prepod_login=callback.data[15:],
            type="l-classes",
            weekday=int(callback.data[13:14]),
            next="next" in callback.data
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-weekly" in callback.data
)
def weekly_lecturer_schedule(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    for weekday in WEEKDAYS:
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text=get_lecturers_schedule(
                prepod_login=callback.data[14:],
                type="l-classes",
                weekday=weekday,
                next="next" in callback.data
            ),
            parse_mode="Markdown"
        )
    
    students[callback.message.chat.id].previous_message = None
    
    hide_loading_notification(id=callback.id)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-exams" in callback.data
)
def send_lecturers_exams(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=get_lecturers_schedule(
            prepod_login=callback.data.replace("l-exams ", ""),
            type="l-exams"
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None
    
    hide_loading_notification(id=callback.id)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/lecturers")
def gs_lecturers(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
