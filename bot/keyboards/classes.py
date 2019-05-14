from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.constants import WEEKDAYS
from bot.constants import MONTHS

from datetime import datetime
from datetime import timedelta


def schedule_type():
    schedule_type_keyboard = InlineKeyboardMarkup()
    
    schedule_type_keyboard.row(
        InlineKeyboardButton(text="сегодня", callback_data="daily crnt {}".format(datetime.today().isoweekday())),
        InlineKeyboardButton(text="завтра", callback_data="daily crnt {}".format(datetime.today().isoweekday() + 1))
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю", callback_data="weekdays crnt"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю", callback_data="weekdays next"))
    
    return schedule_type_keyboard

def certain_date_chooser(todays_weekday, type):
    certain_date_keyboard = InlineKeyboardMarkup()
    
    certain_date_keyboard.row(InlineKeyboardButton(text="Показать все", callback_data="weekly {}".format(type)))
    
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
                callback_data="daily {type} {weekday}".format(type=type, weekday=weekday)
            )
        )
    
    return certain_date_keyboard
