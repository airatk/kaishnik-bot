from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.score import subject_chooser
from bot.keyboards.score import semester_dialer

from bot.helpers import get_subject_score


@kbot.message_handler(
    commands=["score"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("score")
def score(message):
    students[message.chat.id].previous_message = "/score"  # Gate System (GS)
    
    if "экз" in message.text: students[message.chat.id].previous_message += " exams"
    elif "зач" in message.text: students[message.chat.id].previous_message += " tests"
        
    if students[message.chat.id].student_card_number == "unset":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Номер зачётки не указан, но ты можешь это исправить — отправь /card"
        )
    
        students[message.chat.id].previous_message = None  # Gate System (GS)
    elif students[message.chat.id].institute_id == "КИТ":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )

        students[message.chat.id].previous_message = None  # Gate System (GS)
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Выбери номер семестра:",
            reply_markup=semester_dialer(int(students[message.chat.id].year)*2 + 1)
        )

@kbot.callback_query_handler(
    func=lambda callback: (
        students[callback.message.chat.id].previous_message == "/score exams" or
        students[callback.message.chat.id].previous_message == "/score tests"
    ) and "semester" in callback.data
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
    elif scoretable != []:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        subjects_num = 0
        
        mask = "экзамен" if students[callback.message.chat.id].previous_message == "/score exams" else "зачёт"
        
        for subject in range(len(scoretable)):
            subject_score = get_subject_score(scoretable=scoretable, subjects_num=subject)
            
            if mask in subject_score:
                kbot.send_message(
                    chat_id=callback.message.chat.id,
                    text=subject_score,
                    parse_mode="Markdown"
                )

                subjects_num += 1

        if subjects_num == 1: grammatical_entity = ""
        elif subjects_num > 1 and subjects_num < 5: grammatical_entity = "а"
        else: grammatical_entity = "ов"

        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="*{}* предмет{} всего!".format(subjects_num, grammatical_entity),
            parse_mode="Markdown"
        )
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
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
    elif scoretable != []:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выбери предмет:",
            reply_markup=subject_chooser(scoretable=scoretable, semester=semester_number)
        )
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )
        
        students[callback.message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/score" and
        "scoretable all" in callback.data
)
@top_notification
def show_all_score(callback):
    callback_data = callback.data.replace("scoretable all ", "").split()
    
    scoretable = students[callback.message.chat.id].get_scoretable(callback_data[1])
    
    if scoretable is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    elif scoretable != []:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        subjects_num = int(callback_data[0])
        
        for subject in range(subjects_num):
            kbot.send_message(
                chat_id=callback.message.chat.id,
                text=get_subject_score(scoretable=scoretable, subjects_num=subject),
                parse_mode="Markdown"
            )

        if subjects_num == 1: grammatical_entity = ""
        elif subjects_num > 1 and subjects_num < 5: grammatical_entity = "а"
        else: grammatical_entity = "ов"

        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="*{}* предмет{} всего!".format(subjects_num, grammatical_entity),
            parse_mode="Markdown"
        )
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/score" and
        "scoretable" in callback.data
)
@top_notification
def show_score(callback):
    callback_data = callback.data.replace("scoretable ", "").split()
    scoretable = students[callback.message.chat.id].get_scoretable(callback_data[1])
    
    if scoretable is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    elif scoretable != []:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=get_subject_score(scoretable=scoretable, subjects_num=int(callback_data[0])),
            parse_mode="Markdown"
        )
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Нет данных."
        )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/score")
def gs_score(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
