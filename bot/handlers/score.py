from bot import kaishnik
from bot import students

from bot.keyboards import subject_chooser
from bot.keyboards import semester_dailer

from bot.helpers import get_subject_score

@kaishnik.message_handler(commands=["score"])
def score(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
        
    if students[message.chat.id].get_student_card_number() is None:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Номер зачётки не указан, но ты можешь это исправить — отправь /card"
        )
    elif students[message.chat.id].get_institute() == "КИТ":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Выбери номер семестра:",
            reply_markup=semester_dailer(int(students[message.chat.id].get_year())*2 + 1)
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "s_r" in callback.data
)
def s_r(callback):
    try:
        # There might be no data for the certain semester
        if students[callback.message.chat.id].get_score_table(callback.data[4:]) is None:
            kaishnik.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Нет данных."
            )
        else:
            kaishnik.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Выбери предмет:",
                reply_markup=subject_chooser(
                    score_table=students[callback.message.chat.id].get_score_table(callback.data[4:]),
                    semester=callback.data[4:]
                )
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
        "s_t all" in callback.data
)
def show_all_score(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    callback_data = callback.data[8:].split()
    
    try:
        for subject in range(int(callback_data[0])):
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text=get_subject_score(
                    score_table=students[callback.message.chat.id].get_score_table(callback_data[1]),
                    subjects_num=subject
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
        "s_t" in callback.data
)
def show_score(callback):
    callback_data = callback.data[4:].split()
    
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=get_subject_score(
                score_table=students[callback.message.chat.id].get_score_table(callback_data[1]),
                subjects_num=int(callback_data[0])
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

