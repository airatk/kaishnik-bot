from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.constants import WEEKDAYS

from bot.keyboards.classes import schedule_type
from bot.keyboards.classes import certain_date_chooser

from datetime import datetime
from re import fullmatch


@kbot.message_handler(
    commands=["classes"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("classes")
def classes(message):
    students[message.chat.id].previous_message = "/classes"  # Gate System (GS)
    
    if fullmatch("[1-59][1-6][0-9][0-9]", message.text.replace("/classes ", "")):
        students[message.chat.id].another_group_number_schedule = message.text.replace("/classes ", "")
        
        if students[message.chat.id].another_group_number_schedule is None:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
            
            students[message.chat.id].previous_message = None  # Gate System (GS)
            return
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Тебе нужно расписание на:",
        reply_markup=schedule_type()
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/classes" and
        "daily" in callback.data
)
def one_day_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=students[callback.message.chat.id].get_schedule(
            type="classes",
            weekday=int(callback.data[11:]),
            next="next" in callback.data
        ),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].another_group_number_schedule = None
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
    
    top_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/classes" and
        "weekdays" in callback.data
)
def certain_date_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=certain_date_chooser(datetime.today().isoweekday(), callback.data.replace("weekdays ", ""))
    )
    
    top_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/classes" and
        "weekly" in callback.data
)
def weekly_schedule(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    for weekday in WEEKDAYS:
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text=students[callback.message.chat.id].get_schedule(
                type="classes",
                weekday=weekday,
                next="next" in callback.data
            ),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    
    students[callback.message.chat.id].another_group_number_schedule = None
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
    
    top_notification(id=callback.id)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/classes")
def gs_classes(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@kbot.message_handler(
    commands=["exams"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("exams")
def exams(message):
    if fullmatch("[1-59][1-6][0-9][0-9]", message.text.replace("/exams ", "")):
        students[message.chat.id].another_group_number_schedule = message.text.replace("/exams ", "")
        
        if students[message.chat.id].another_group_number_schedule is None:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
            
            students[message.chat.id].previous_message = None  # Gate System (GS)
            return

    kbot.send_message(
        chat_id=message.chat.id,
        text=students[message.chat.id].get_schedule(type="exams"),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    students[message.chat.id].another_group_number_schedule = None
