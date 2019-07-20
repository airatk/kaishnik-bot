from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.helpers.datatypes import ScheduleType
from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import MONTHS

from datetime import datetime
from datetime import timedelta


def choose_lecturer(names):
    choose_lecturer_keyboard = InlineKeyboardMarkup(row_width=1)

    choose_lecturer_keyboard.add(*[
        InlineKeyboardButton(
            text=name["lecturer"],
            callback_data="lecturer {}".format(name["id"])
        ) for name in names
    ])
    
    return choose_lecturer_keyboard

def lecturer_info_type(lecturer_id):
    lecturer_info_type_keyboard = InlineKeyboardMarkup(row_width=1)
    
    lecturer_info_type_keyboard.add(
        InlineKeyboardButton(text="занятия", callback_data=" ".join([ ScheduleType.classes.value, lecturer_id ])),
        InlineKeyboardButton(text="экзамены", callback_data=" ".join([ ScheduleType.exams.value, lecturer_id ]))
    )
    
    return lecturer_info_type_keyboard

def lecturer_classes_week_type(lecturer_id):
    week_type_keyboard = InlineKeyboardMarkup(row_width=1)
    
    week_type_keyboard.add(
        InlineKeyboardButton(text="текущую неделю", callback_data="l-weekdays crnt {}".format(lecturer_id)),
        InlineKeyboardButton(text="следующую неделю", callback_data="l-weekdays next {}".format(lecturer_id))
    )
    
    return week_type_keyboard

def lecturer_certain_date_chooser(todays_weekday, type, lecturer_id):
    certain_date_keyboard = InlineKeyboardMarkup()
    
    certain_date_keyboard.row(InlineKeyboardButton(text="Показать все", callback_data="l-weekly {} {}".format(type, lecturer_id)))
    
    today = datetime.today()
    
    for weekday in WEEKDAYS:
        date = today + timedelta(days=(weekday - todays_weekday) + (7 if type == "next" else 0))
        
        certain_date_keyboard.row(
            InlineKeyboardButton(
                text="{weekday}, {day} {month}{is_today}".format(
                    weekday=WEEKDAYS[weekday],
                    day=int(date.strftime("%d")),
                    month=MONTHS[date.strftime("%m")],
                    is_today=" •" if today.strftime("%d") == date.strftime("%d") else ""
                ),
                callback_data="l-daily {type} {weekday} {lecturer_id}".format(
                    type=type,
                    weekday=weekday,
                    lecturer_id=lecturer_id
                )
            )
        )
    
    return certain_date_keyboard
