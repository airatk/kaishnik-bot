from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.lecturers import choose_lecturer
from bot.keyboards.lecturers import lecturer_info_type

from bot.helpers.lecturers import get_lecturers_names
from bot.helpers.constants import MAX_LECTURERS_NUMBER
from bot.helpers.constants import LOADING_REPLIES

from random import choice


@kbot.message_handler(
    commands=["lecturers"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("lecturers")
def lecturers(message):
    students[message.chat.id].previous_message = "/lecturers name"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Отправь фамилию или ФИО преподавателя."
    )

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/lecturers name")
def find_lecturer(message):
    # Cleanning the chat
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try:
        kbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id - 1,
            text=choice(LOADING_REPLIES)
        )
    except Exception:
        kbot.send_message(
            chat_id=message.chat.id,
            text=choice(LOADING_REPLIES)
        )
    
    names = get_lecturers_names(name_part=message.text)
    
    # Cleanning the chat
    try: kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception: pass
    
    if names is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[message.chat.id].previous_message = None  # Gate System (GS)
        return

    if names == []:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Ничего не найдено :("
        )
        
        students[message.chat.id].previous_message = None  # Gate System (GS)
        return

    if len(names) > MAX_LECTURERS_NUMBER:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Слишком мало букв, слишком много преподавателей…"
        )
        
        students[message.chat.id].previous_message = None  # Gate System (GS)
        return

    kbot.send_message(
        chat_id=message.chat.id,
        text="Выбери преподавателя:",
        reply_markup=choose_lecturer(names=names)
    )
    
    students[message.chat.id].previous_message = "/lecturers"  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "lecturer" in callback.data
)
@top_notification
def lecturers_schedule_type(callback):
    lecturer_id = callback.data.split()[1]
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужны преподавателевы:",
        reply_markup=lecturer_info_type(lecturer_id=lecturer_id)
    )


# Importing respective lecturers menu options
from bot.handlers.lecturers import classes
from bot.handlers.lecturers import exams


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/lecturers")
def gs_lecturers(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
