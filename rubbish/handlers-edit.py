from bot import kaishnik
from bot import students
from bot import metrics
from bot import on_callback_query

from bot.subject import StudentSubject

from bot.constants import WEEKDAYS

from bot.keyboards.edit import week_chooser
from bot.keyboards.edit import weekday_chooser
from bot.keyboards.edit import edit_dailer
from bot.keyboards.edit import classes_beginning_dailer
from bot.keyboards.edit import buildings_dailer
from bot.keyboards.edit import non_auditorium_chooser

from re import fullmatch

@kaishnik.message_handler(commands=["edit"])
def edit(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("edit")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Выбери неделю, чтобы скорректировать расписание или сбросить изменения:",
        reply_markup=week_chooser()
    )

@kaishnik.callback_query_handler(func=lambda callback: "edit-week-" in callback.data)
def edit_on_week(callback):
    students[callback.message.chat.id].path_to_edited["weektype"] = callback.data.replace("edit-week-", "")
    
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери день недели:",
        reply_markup=weekday_chooser()
    )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: "edit-weekday-" in callback.data)
def edit_on_weekday(callback):
    students[callback.message.chat.id].path_to_edited["weekday"] = int(callback.data.replace("edit-weekday-", ""))
    weekday = WEEKDAYS[int(callback.data.replace("edit-weekday-", ""))].lower().replace("а", "у")
    # lower() is for aesthetics purposes & replace() is for abiding by Russian grammar rules
    
    weektype_key = students[callback.message.chat.id].path_to_edited["weektype"]
    weekday_key = students[callback.message.chat.id].path_to_edited["weekday"]
    
    number = len(students[callback.message.chat.id].edited_subjects[weektype_key][weekday_key])
    
    try:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Количество отредактированных предметов на *{weekday}* — *{number}*.".format(
                weekday=weekday,
                number=number
            ),
            reply_markup=edit_dailer(is_non_edited=number == 0),
            parse_mode="Markdown"
        )
    except KeyError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Воу! Что-то пошло не так😰"
        )
    
    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "cancel-edit")
def cancel_edit(callback):
    students[callback.message.chat.id].path_to_edited["weektype"] = ""
    students[callback.message.chat.id].path_to_edited["weekday"] = 0
    
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отменено!"
    )
    
    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "more-edit")
def choose_begin_time(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери время начала пары:",
        reply_markup=classes_beginning_dailer()
    )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: "edit-begin-time-" in callback.data)
def choose_building_set_begin_time(callback):
    try:
        weektype_key = students[callback.message.chat.id].path_to_edited["weektype"]
        weekday_key = students[callback.message.chat.id].path_to_edited["weekday"]
        
        students[callback.message.chat.id].path_to_edited["hour"] = callback.data.replace("edit-begin-time-", "").split(":")[0]
        hour_key = callback.data.replace("edit-begin-time-", "").split(":")[0]
        
        students[callback.message.chat.id].edited_subjects[weektype_key][weekday_key][hour_key] = StudentSubject()
        students[callback.message.chat.id].edited_subjects[weektype_key][weekday_key][hour_key].set_time(
            callback.data.replace("edit-begin-time-", "")
        )
        
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выбери здание:",
            reply_markup=buildings_dailer()
        )
    except KeyError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Воу! Что-то пошло не так😰"
        )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: "edit-building-" in callback.data)
def choose_auditorium_set_building(callback):
    try:
        weektype_key = students[callback.message.chat.id].path_to_edited["weektype"]
        weekday_key = students[callback.message.chat.id].path_to_edited["weekday"]
        hour_key = students[callback.message.chat.id].path_to_edited["hour"]
        
        students[callback.message.chat.id].edited_subjects[weektype_key][weekday_key][hour_key].set_building(
            callback.data.replace("edit-building-", "")
        )
        
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Отправь номер аудитории либо выбери один из вариантов:",
            reply_markup=non_auditorium_chooser()
        )
        
        students[callback.message.chat.id].previous_message = "/edit auditorium"
    except KeyError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Воу! Что-то пошло не так😰"
        )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit auditorium" and (
            callback.data == "каф" or callback.data == "вц"
        )
)
@kaishnik.message_handler(
    func=lambda message:
        students[message.chat.id].previous_message == "/edit auditorium" and fullmatch("[0-9][0-9][0-9]а?", message.text)
)
def take_teacher_set_auditorium(message):
    weektype_key = students[message.chat.id].path_to_edited["weektype"]
    weekday_key = students[message.chat.id].path_to_edited["weekday"]
    hour_key = students[message.chat.id].path_to_edited["hour"]
    
    try:
        message = callback.message
        
        students[callback.message.chat.id].edited_subjects[weektype_key][weekday_key][hour_key].set_auditorium(callback.data)
    except Exception:
        message = callback

        students[callback.chat.id].edited_subjects[weektype_key][weekday_key][hour_key].set_auditorium(message.text)
    
    kaishnik.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Отправь имя преподавателя."
    )

    students[message.chat.id].previous_message = "/edit teacher"

    try:
        on_callback_query(id=message.id)
    except Exception:
        pass

@kaishnik.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit teacher")
def take_department_set_teacher(message):
    weektype_key = students[message.chat.id].path_to_edited["weektype"]
    weekday_key = students[message.chat.id].path_to_edited["weekday"]
    hour_key = students[message.chat.id].path_to_edited["hour"]
    
    students[message.chat.id].edited_subjects[weektype_key][weekday_key][hour_key].set_teacher(message.text)
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Отправь название кафедры."
    )
    
    students[message.chat.id].previous_message = "/edit department"

@kaishnik.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit department")
def set_department_finish_edit(message):
    weektype_key = students[message.chat.id].path_to_edited["weektype"]
    weekday_key = students[message.chat.id].path_to_edited["weekday"]
    hour_key = students[message.chat.id].path_to_edited["hour"]
    
    students[message.chat.id].edited_subjects[weektype_key][weekday_key][hour_key].set_department(message.text)
    
    students[message.chat.id].previous_message = None
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Отредактировано!"
    )

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "drop-edited-edit")
def drop_edited_subject(callback):
    pass

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "drop-edit")
def drop_edit(callback):
    try:
        weektype_key = students[callback.message.chat.id].path_to_edited["weektype"]
        weekday_key = students[callback.message.chat.id].path_to_edited["weekday"]

        students[callback.message.chat.id].path_to_edited["weektype"] = ""
        students[callback.message.chat.id].path_to_edited["weekday"] = 0
        
        students[callback.message.chat.id].edited_subjects[weektype_key][weekday_key] = {}
        
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сброшено!"
        )
    except KeyError:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Воу! Что-то пошло не так😰"
        )

    on_callback_query(id=callback.id)
