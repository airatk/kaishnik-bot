from bot import kaishnik
from bot import students
from bot import metrics

from bot.constants import WEEK

from bot.keyboards.schedule import choose_lecturer
from bot.keyboards.schedule import lecturer_schedule_type
from bot.keyboards.schedule import lecturer_classes_week_type
from bot.keyboards.schedule import schedule_type
from bot.keyboards.schedule import certain_date_chooser
from bot.keyboards.schedule import lecturer_certain_date_chooser

from bot.helpers import get_lecturers_names
from bot.helpers import get_lecturers_schedule
from bot.helpers import get_week

from datetime import datetime
from json.decoder import JSONDecodeError


@kaishnik.message_handler(commands=["lecturers"])
def lecturers(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("lecturers")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Введи ФИО преподавателя полностью или частично."
    )
    
    students[message.chat.id].previous_message = message.text

@kaishnik.message_handler(
    func=lambda message:
        students[message.chat.id].previous_message == "/lecturers",
    content_types=["text"]
)
def find_lecturer(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # In case kai.ru is down
    try:
        names = get_lecturers_names(message.text)
    except JSONDecodeError:
        names = None
    
    if names is None:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )
    elif names == []:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Ничего не найдено :("
        )
    else:
        try:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Выбери преподавателя:",
                reply_markup=choose_lecturer(names)
            )
        except Exception:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Слишком мало букв, слишком много преподавателей…"
            )
    
    students[message.chat.id].previous_message = None

@kaishnik.callback_query_handler(
    func=lambda callback:
        "lecturer" in callback.data
)
def lecturers_schedule_type(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужно преподавателево расписание:",
        reply_markup=lecturer_schedule_type(callback.data.replace("lecturer ", ""))
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l-classes" in callback.data
)
def lecturers_week_type_classes(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Преподавателево расписание занятий на:",
        reply_markup=lecturer_classes_week_type(callback.data.replace("l-classes ", ""))
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l-weekdays" in callback.data
)
def certain_date_schedule(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=lecturer_certain_date_chooser(
            todays_weekday=datetime.today().isoweekday(),
            type=callback.data.replace("l-weekdays ", "")[:4],
            prepod_login=callback.data[16:]
        )
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l-daily" in callback.data
)
def one_day_lecturer_schedule(callback):
    try:
        kaishnik.edit_message_text(
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
    except JSONDecodeError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l-weekly" in callback.data
)
def weekly_lecturer_schedule(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    try:
        for weekday in WEEK:
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text=get_lecturers_schedule(
                    prepod_login=callback.data[14:],
                    type="l-classes",
                    weekday=weekday,
                    next="next" in callback.data
                ),
                parse_mode="Markdown"
            )
    except JSONDecodeError:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l-exams" in callback.data
)
def send_lecturers_exams(callback):
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=get_lecturers_schedule(
                prepod_login=callback.data.replace("l-exams ", ""),
                type="l-exams"
            ),
            parse_mode="Markdown"
        )
    except JSONDecodeError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )


@kaishnik.message_handler(commands=["classes"])
def classes(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("classes")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Тебе нужно расписание на:",
        reply_markup=schedule_type()
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "weekdays" in callback.data
)
def certain_date_schedule(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=certain_date_chooser(datetime.today().isoweekday(), callback.data.replace("weekdays ", ""))
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "daily" in callback.data
)
def one_day_schedule(callback):
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=students[callback.message.chat.id].get_schedule(
                type="classes",
                weekday=int(callback.data[11:]),
                next="next" in callback.data
            ),
            parse_mode="Markdown"
        )
    except JSONDecodeError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "weekly" in callback.data
)
def weekly_schedule(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    try:
        for weekday in WEEK:
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text=students[callback.message.chat.id].get_schedule(
                    type="classes",
                    weekday=weekday,
                    next="next" in callback.data
                ),
                parse_mode="Markdown"
            )
    except JSONDecodeError:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )


@kaishnik.message_handler(commands=["exams"])
def exams(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("exams")
    
    try:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text=students[message.chat.id].get_schedule(type="exams"),
            parse_mode="Markdown"
        )
    except JSONDecodeError:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )


@kaishnik.message_handler(commands=["week"])
def week(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("week")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=get_week()
    )
