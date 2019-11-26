from bot import bot
from bot import students

from bot.commands.edit.utilities.keyboards import skip
from bot.commands.edit.utilities.keyboards import weektype_editer
from bot.commands.edit.utilities.keyboards import weekday_editer
from bot.commands.edit.utilities.keyboards import hours_editer
from bot.commands.edit.utilities.keyboards import buildings_editer
from bot.commands.edit.utilities.keyboards import subject_type_editer

from bot.shared.keyboards import cancel_option
from bot.shared.helpers import top_notification
from bot.shared.api.subject import StudentSubject
from bot.shared.calendar.week import WeekParity
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        callback.data == Commands.EDIT_ADD.value
)
@top_notification
def add_edit(callback):
    students[callback.message.chat.id].edited_subject = StudentSubject()
    students[callback.message.chat.id].edited_subject.dates = ""
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери тип недели:",
        reply_markup=weektype_editer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_WEEKTYPE.value in callback.data
)
@top_notification
def add_weekday(callback):
    weektype = callback.data.split()[1]
    
    if weektype != WeekParity.BOTH.value:
        students[callback.message.chat.id].edited_subject.is_even = weektype == WeekParity.EVEN.value
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери день:",
        reply_markup=weekday_editer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_WEEKDAY.value in callback.data
)
@top_notification
def add_time(callback):
    students[callback.message.chat.id].edited_subject.weekday = int(callback.data.split()[1])
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери время начала пары:",
        reply_markup=hours_editer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_TIME.value in callback.data
)
@top_notification
def add_building(callback):
    students[callback.message.chat.id].edited_subject.time = callback.data.split()[1]
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери учебное здание:",
        reply_markup=buildings_editer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_BUILDING.value in callback.data
)
@top_notification
def add_auditorium(callback):
    students[callback.message.chat.id].edited_subject.building = callback.data.split()[1]
    
    guard_message = bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер аудитории (или где там у тебя пара).",
        reply_markup=skip(ACTION=Commands.EDIT_AUDITORIUM)
    )
    
    students[callback.message.chat.id].guard.text = Commands.EDIT_AUDITORIUM.value
    students[callback.message.chat.id].guard.message = guard_message

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT_AUDITORIUM.value and
        callback.data == Commands.EDIT_AUDITORIUM.value
)
@top_notification
def skip_auditorium(callback):
    students[callback.message.chat.id].edited_subject.auditorium = ""
    add_subject_title(callback.message)

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.EDIT_AUDITORIUM.value)
def add_subject_title(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    if students[message.chat.id].edited_subject.auditorium != "":
        bot.delete_message(chat_id=students[message.chat.id].guard.message.chat.id, message_id=students[message.chat.id].guard.message.message_id)
        
        students[message.chat.id].edited_subject.auditorium = message.text
    
    guard_message = bot.send_message(
        chat_id=message.chat.id,
        text="Отправь название предмета.",
        reply_markup=cancel_option()
    )
    
    students[message.chat.id].guard.text = Commands.EDIT_SUBJECT_TITLE.value
    students[message.chat.id].guard.message = guard_message

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.EDIT_SUBJECT_TITLE.value)
def add_subject_type(message):
    students[message.chat.id].edited_subject.title = message.text
    
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text="Выбери тип предмета:",
        reply_markup=subject_type_editer()
    )
    
    students[message.chat.id].guard.text = Commands.EDIT.value

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_SUBJECT_TYPE.value in callback.data
)
@top_notification
def add_lecturer(callback):
    students[callback.message.chat.id].edited_subject.type = callback.data.split()[1]
    
    guard_message = bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь имя преподавателя.",
        reply_markup=skip(ACTION=Commands.EDIT_LECTURER)
    )
    
    students[callback.message.chat.id].guard.text = Commands.EDIT_LECTURER.value
    students[callback.message.chat.id].guard.message = guard_message

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT_LECTURER.value and
        callback.data == Commands.EDIT_LECTURER.value
)
@top_notification
def skip_lecturer(callback):
    students[callback.message.chat.id].edited_subject.lecturer = ""
    add_department(callback.message)

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.EDIT_LECTURER.value)
def add_department(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    if students[message.chat.id].edited_subject.lecturer != "":
        bot.delete_message(chat_id=students[message.chat.id].guard.message.chat.id, message_id=students[message.chat.id].guard.message.message_id)
        
        students[message.chat.id].edited_subject.lecturer = message.text
    
    guard_message = bot.send_message(
        chat_id=message.chat.id,
        text="Отправь название кафедры.",
        reply_markup=skip(ACTION=Commands.EDIT_DEPARTMENT)
    )
    
    students[message.chat.id].guard.text = Commands.EDIT_DEPARTMENT.value
    students[message.chat.id].guard.message = guard_message

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT_DEPARTMENT.value and
        callback.data == Commands.EDIT_DEPARTMENT.value
)
@top_notification
def skip_department(callback):
    students[callback.message.chat.id].edited_subject.department = ""
    end_edit(callback.message)

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.EDIT_DEPARTMENT.value)
def end_edit(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    if students[message.chat.id].edited_subject.department != "":
        bot.delete_message(chat_id=students[message.chat.id].guard.message.chat.id, message_id=students[message.chat.id].guard.message.message_id)
        
        students[message.chat.id].edited_subject.department = message.text
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].edited_subjects.append(students[message.chat.id].edited_subject)
    students[message.chat.id].edited_subject = None
    
    save_data(file=USERS_FILE, object=students)
