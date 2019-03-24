from bot import kaishnik
from bot import students

from bot.constants import WEEK

from bot.keyboards import choose_lecturer
from bot.keyboards import lecturer_schedule_type
from bot.keyboards import lecturer_classes_week_type
from bot.keyboards import schedule_type

from bot.helpers import get_lecturers_names
from bot.helpers import get_lecturers_schedule
from bot.helpers import get_week

from datetime import datetime

@kaishnik.message_handler(commands=["lecturers"])
def lecturers(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Введи ФИО преподавателя полностью или частично."
    )
    
    students[message.chat.id].set_pmt(message.text)

@kaishnik.message_handler(
    func=lambda message:
        students[message.chat.id].get_pmt() == "/lecturers",
    content_types=["text"]
)
def find_lecturer(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # In case kai.ru is down
    try:
        names = get_lecturers_names(message.text)
    except:
        names = None
    
    if names is not None:
        try:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Выбери преподавателя:",
                reply_markup=choose_lecturer(names)
            )
        except:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Слишком мало букв, слишком много преподавателей…"
            )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Ничего не найдено :("
        )
    
    students[message.chat.id].set_pmt(None)

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l_r" in callback.data
)
def lecturers_schedule_type(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужно преподавателево расписание:",
        reply_markup=lecturer_schedule_type(callback.data[4:])
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l_c" in callback.data
)
def lecturers_week_type_classes(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Преподавателево расписание занятий на:",
        reply_markup=lecturer_classes_week_type(callback.data[4:])
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "c_w" in callback.data
)
def send_lecturers_classes(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    try:
        for weekday in WEEK:
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text=get_lecturers_schedule(
                    prepod_login=callback.data[9:],
                    type="l_c",
                    weekday=weekday,
                    next="next" in callback.data
                ),
                parse_mode="Markdown"
            )
    except:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "l_e" in callback.data
)
def send_lecturers_exams(callback):
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=get_lecturers_schedule(
                prepod_login=callback.data[4:],
                type=callback.data[:3]
            ),
            parse_mode="Markdown"
        )
    except:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.message_handler(commands=["classes"])
def classes(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Тебе нужно расписание на:",
        reply_markup=schedule_type()
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        callback.data == "today's" or \
        callback.data == "tomorrow's"
)
def one_day_schedule(callback):
    todays_weekday = datetime.today().isoweekday()
    
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=students[callback.message.chat.id].get_schedule(
                type="classes",
                weekday=todays_weekday if callback.data == "today's" else todays_weekday + 1
            ),
            parse_mode="Markdown"
        )
    except:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
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
    except:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.message_handler(commands=["exams"])
def exams(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text=students[message.chat.id].get_schedule(type="exams"),
            parse_mode="Markdown"
        )
    except:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.message_handler(commands=["week"])
def week(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=get_week()
    )
