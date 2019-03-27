from bot import kaishnik
from bot import students

from bot.keyboards import subject_chooser
from bot.keyboards import semester_dailer

from bot.helpers import get_subject_score

from json.decoder import JSONDecodeError

@kaishnik.message_handler(commands=["score"])
def score(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
        
    if students[message.chat.id].student_card_number == "unset":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Номер зачётки не указан, но ты можешь это исправить — отправь /card"
        )
    elif students[message.chat.id].institute_id == "КИТ":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Выбери номер семестра:",
            reply_markup=semester_dailer(int(students[message.chat.id].year)*2 + 1)
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "semester" in callback.data
)
def semester_subjects(callback):
    semester_number = callback.data.replace("semester ", "")
    
    try:
        # There might be no data for the asked semester
        if students[callback.message.chat.id].get_scoretable(semester_number) is not None:
            kaishnik.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Выбери предмет:",
                reply_markup=subject_chooser(
                    scoretable=students[callback.message.chat.id].get_scoretable(semester_number),
                    semester=semester_number
                )
            )
        else:
            kaishnik.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Нет данных."
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
        "scoretable all" in callback.data
)
def show_all_score(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    callback_data = callback.data.replace("scoretable all ", "").split()
    
    try:
        for subject in range(int(callback_data[0])):
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text=get_subject_score(
                    scoretable=students[callback.message.chat.id].get_scoretable(callback_data[1]),
                    subjects_num=subject
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
        "scoretable" in callback.data
)
def show_score(callback):
    callback_data = callback.data.replace("scoretable ", "").split()
    
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=get_subject_score(
                scoretable=students[callback.message.chat.id].get_scoretable(callback_data[1]),
                subjects_num=int(callback_data[0])
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
