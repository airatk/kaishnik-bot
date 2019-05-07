from bot import kbot
from bot import students
from bot import metrics
from bot import hide_loading_notification

from bot.subject import StudentSubject

from bot.constants import MAX_BUTTONS_NUMBER

from bot.keyboards.edit import canceler_skipper
from bot.keyboards.edit import edit_chooser
from bot.keyboards.edit import weektype_dialer
from bot.keyboards.edit import weekday_dialer
from bot.keyboards.edit import hours_dialer
from bot.keyboards.edit import buildings_dialer
from bot.keyboards.edit import subject_type_dialer
from bot.keyboards.edit import delete_edit_chooser
from bot.keyboards.edit import edit_canceler

from bot.helpers import save_to


# /edit menu
@kbot.message_handler(
    commands=["edit"],
    func=lambda message: students[message.chat.id].previous_message is None
)
def edit(message):
    metrics.increment("edit")
    
    students[message.chat.id].previous_message = "/edit"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "Изменить — это одновременно и изменить, и добавить."
            "\n\n"
            "Добавлено-изменено пар: *{}*".format(len(students[message.chat.id].edited_subjects))
        ),
        reply_markup=edit_chooser(),
        parse_mode="Markdown"
    )


# "edit" option
@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        callback.data == "add-edit"
)
def add_edit(callback):
    students[callback.message.chat.id].edited_class = StudentSubject()
    students[callback.message.chat.id].edited_class.dates = ""
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери тип недели:",
        reply_markup=weektype_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "edit-weektype-" in callback.data
)
def edit_weekday(callback):
    students[callback.message.chat.id].edited_class.is_even = callback.data.replace("edit-weektype-", "") == "even"
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери день:",
        reply_markup=weekday_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "edit-weekday-" in callback.data
)
def edit_time(callback):
    students[callback.message.chat.id].edited_class.weekday = int(callback.data.replace("edit-weekday-", ""))
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери время начала пары:",
        reply_markup=hours_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "edit-time-" in callback.data
)
def edit_building(callback):
    students[callback.message.chat.id].edited_class.time = callback.data.replace("edit-time-", "")
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери учебное здание:",
        reply_markup=buildings_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "edit-building-" in callback.data
)
def edit_auditorium(callback):
    students[callback.message.chat.id].edited_class.building = callback.data.replace("edit-building-", "")
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер аудитории (или где там пара у тебя).",
        reply_markup=edit_canceler()
    )
    
    students[callback.message.chat.id].previous_message = "/edit auditorium"  # Gate System (GS)
    
    hide_loading_notification(id=callback.id)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit auditorium")
def edit_subject_title(message):
    students[message.chat.id].edited_class.auditorium = message.text
    
    # Cleanning the chat
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Отправь название предмета.",
        reply_markup=edit_canceler()
    )

    students[message.chat.id].previous_message = "/edit subject-title"  # Gate System (GS)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit subject-title")
def edit_subject_type(message):
    students[message.chat.id].edited_class.title = message.text
    
    # Cleanning the chat
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Выбери тип предмета:",
        reply_markup=subject_type_dialer()
    )

    students[message.chat.id].previous_message = "/edit"  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "edit-subject-type-" in callback.data
)
def edit_lecturer_name(callback):
    students[callback.message.chat.id].edited_class.type = callback.data.replace("edit-subject-type-", "")
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь имя преподавателя.",
        reply_markup=canceler_skipper(callback_data="edit-teacher-name-")
    )
    
    students[callback.message.chat.id].previous_message = "/edit teacher-name"  # Gate System (GS)
    
    hide_loading_notification(id=callback.id)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit teacher-name")
@kbot.callback_query_handler(func=lambda callback: callback.data == "edit-teacher-name-")
def edit_department(callback):
    try:
        message = callback.message
    except Exception:
        message = callback
        
        # Cleanning the chat
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        
        students[message.chat.id].edited_class.teacher = message.text
    else:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
        students[message.chat.id].edited_class.teacher = ""

    kbot.send_message(
        chat_id=message.chat.id,
        text="Отправь название кафедры.",
        reply_markup=canceler_skipper(callback_data="edit-department-")
    )

    students[message.chat.id].previous_message = "/edit department"  # Gate System (GS)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit department")
@kbot.callback_query_handler(func=lambda callback: callback.data == "edit-department-")
def finish_edit(callback):
    try:
        message = callback.message
    except Exception:
        message = callback
        
        # Cleanning the chat
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        
        students[message.chat.id].edited_class.department = message.text
    else:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        students[message.chat.id].edited_class.department = ""

    students[message.chat.id].edited_subjects.append(students[message.chat.id].edited_class)
    students[message.chat.id].edited_class = None
    
    students[message.chat.id].previous_message = None  # Gate System (GS)
    
    save_to(filename="data/users", object=students)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )


# "delete" option
@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        callback.data == "delete-edit"
)
def delete_edit(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    edited_subjects = students[callback.message.chat.id].edited_subjects
    
    if edited_subjects != []:
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="Выбери пару, которую нужно удалить:",
            reply_markup=delete_edit_chooser(edited_subjects)
        )
    else:
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="Добавленных пар нет."
        )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "delete-edit-" in callback.data
)
def delete_edited(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    if "all" in callback.data:
        students[callback.message.chat.id].edited_subjects = []
    else:
        del students[callback.message.chat.id].edited_subjects[int(callback.data.replace("delete-edit-number-", ""))]
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
    
    save_to(filename="data/users", object=students)
    
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="Удалено!"
    )


# helpers
@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        callback.data == "cancel-edit"
)
def cancel_edit(callback):
    students[callback.message.chat.id].edited_class = None
    
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="Отменено!"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
    
    hide_loading_notification(id=callback.id)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit")
def gs_edit(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
