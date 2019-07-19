from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.score import subject_chooser
from bot.keyboards.score import semester_dialer

from bot.helpers           import get_subject_score
from bot.helpers.constants import LOADING_REPLIES

from random import choice


@kbot.message_handler(
    commands=["score"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("score")
def score(message):
    if students[message.chat.id].student_card_number == "unset":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Номер зачётки не указан, но ты можешь это исправить — отправь /card"
        )
        return

    if students[message.chat.id].institute_id == "КИТ":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
        return
    
    last_available_semester = students[message.chat.id].get_last_available_semester()

    if last_available_semester is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        return

    students[message.chat.id].previous_message = "/score"  # Gate System (GS)

    if "экз" in message.text:
        students[message.chat.id].previous_message += " exams"
    elif "зач" in message.text:
        students[message.chat.id].previous_message += " tests"

        if "оц" in message.text:
            students[message.chat.id].previous_message += " plus"

    kbot.send_message(
        chat_id=message.chat.id,
        text="Выбери номер семестра:",
        reply_markup=semester_dialer(last_available_semester)
    )

@kbot.callback_query_handler(
    func=lambda callback: (
        students[callback.message.chat.id].previous_message is not None and
        students[callback.message.chat.id].previous_message.startswith("/score") and
        "semester" in callback.data and (
            "exams" in students[callback.message.chat.id].previous_message or
            "tests" in students[callback.message.chat.id].previous_message
        )
    )
)
@top_notification
def show_all_score(callback):
    semester_number = callback.data.replace("semester ", "")
    scoretable = students[callback.message.chat.id].get_scoretable(semester_number)
    
    if scoretable is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    if scoretable == []:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )
        
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    subjects_num = 0
    
    if "exams" in students[callback.message.chat.id].previous_message:
        mask = "экзамен"
    elif "tests" in students[callback.message.chat.id].previous_message:
        mask = "зачёт"

        if "plus" in students[callback.message.chat.id].previous_message:
            mask += " с оценкой"
    
    for subject in range(len(scoretable)):
        subject_score = get_subject_score(scoretable=scoretable, subjects_num=subject)
        
        if mask in subject_score:
            kbot.send_message(
                chat_id=callback.message.chat.id,
                text=subject_score,
                parse_mode="Markdown"
            )

            subjects_num += 1

    if subjects_num == 1:
        grammatical_entity = ""
    elif subjects_num > 1 and subjects_num < 5:
        grammatical_entity = "а"
    else:
        grammatical_entity = "ов"

    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="*{}* предмет{} всего!".format(subjects_num, grammatical_entity),
        parse_mode="Markdown"
    )

    students[callback.message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/score" and
        "semester" in callback.data
)
@top_notification
def semester_subjects(callback):
    semester_number = callback.data.replace("semester ", "")
    scoretable = students[callback.message.chat.id].get_scoretable(semester_number)
    
    if scoretable is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    if scoretable == []:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )
        
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери предмет:",
        reply_markup=subject_chooser(scoretable=scoretable, semester=semester_number)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/score" and
        "scoretable all" in callback.data
)
@top_notification
def show_all_score(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data = callback.data.replace("scoretable all ", "").split()
    scoretable = students[callback.message.chat.id].get_scoretable(callback_data[1])
    
    if scoretable is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    if scoretable == []:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )

        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    subjects_num = int(callback_data[0])
    
    for subject in range(subjects_num):
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text=get_subject_score(scoretable=scoretable, subjects_num=subject),
            parse_mode="Markdown"
        )

    if subjects_num == 1:
        grammatical_entity = ""
    elif subjects_num > 1 and subjects_num < 5:
        grammatical_entity = "а"
    else:
        grammatical_entity = "ов"

    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="*{}* предмет{} всего!".format(subjects_num, grammatical_entity),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/score" and
        "scoretable" in callback.data
)
@top_notification
def show_score(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data = callback.data.replace("scoretable ", "").split()
    scoretable = students[callback.message.chat.id].get_scoretable(callback_data[1])
    
    if scoretable is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    if scoretable == []:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )
    
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
        
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=get_subject_score(scoretable=scoretable, subjects_num=int(callback_data[0])),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/score")
def gs_score(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
