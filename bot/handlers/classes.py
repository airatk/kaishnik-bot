from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.classes import schedule_type
from bot.keyboards.classes import certain_date_chooser

from bot.helpers.datatypes import ScheduleType
from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import LOADING_REPLIES

from datetime import datetime
from random import choice
from re import fullmatch


@kbot.message_handler(
    commands=["classes"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("classes")
def classes(message):
    students[message.chat.id].previous_message = "/classes"  # Gate System (GS)
    
    another_group = message.text.replace("/classes", "")
    
    if another_group != "":
        another_group = another_group[1:]  # Getting rid of a whitespace
        
        if not fullmatch("[1-59][1-6][0-9][0-9]", another_group):
            kbot.send_message(
                chat_id=message.chat.id,
                text="Неверный номер группы. Исправляйся."
            )
            
            students[message.chat.id].previous_message = None  # Gate System (GS)
            return
        
        students[message.chat.id].another_group_number_schedule = another_group
    
        if students[message.chat.id].another_group_number_schedule is None:
            kbot.send_message(
                chat_id=message.chat.id,
                text="kai.ru не отвечает🤷🏼‍♀️",
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
@top_notification
def one_day_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    callback_data = callback.data.split()
    
    schedule = students[callback.message.chat.id].get_schedule(
        type=ScheduleType.classes,
        next="next" in callback_data
    )
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=schedule[int(callback_data[2]) - 1] if len(schedule) != 1 else schedule[0],
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].another_group_number_schedule = None
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/classes" and
        "weekdays" in callback.data
)
@top_notification
def certain_date_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=certain_date_chooser(datetime.today().isoweekday(), callback.data.replace("weekdays ", ""))
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/classes" and
        "weekly" in callback.data
)
@top_notification
def weekly_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    schedule = students[callback.message.chat.id].get_schedule(
        type=ScheduleType.classes,
        next="next" in callback.data
    )
    
    if len(schedule) == 1:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=schedule[0]
        )
    else:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        for weekday in WEEKDAYS:
            kbot.send_message(
                chat_id=callback.message.chat.id,
                text=schedule[weekday - 1],
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    
    students[callback.message.chat.id].another_group_number_schedule = None
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/classes")
def gs_classes(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
