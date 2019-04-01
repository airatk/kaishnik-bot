from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot import students

from bot.constants import WEEKDAYS
from bot.constants import BUILDINGS

from datetime import datetime
from datetime import timedelta

def week_chooser():
    week_chooser_keyboard = InlineKeyboardMarkup()
    
    week_chooser_keyboard.row(InlineKeyboardButton(text="чётная", callback_data="edit-week-even"))
    week_chooser_keyboard.row(InlineKeyboardButton(text="нечётная", callback_data="edit-week-odd"))
    
    return week_chooser_keyboard

def weekday_chooser():
    weekday_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    weekday_chooser_keyboard.add(*[
        InlineKeyboardButton(text=WEEKDAYS[weekday], callback_data="edit-weekday-{}".format(weekday)) for weekday in WEEKDAYS
    ])
    
    return weekday_chooser_keyboard

def edit_dailer(is_non_edited):
    edit_dailer_keyboard = InlineKeyboardMarkup()
    
    edit_dailer_keyboard.row(InlineKeyboardButton(
        text="Редактировать{}".format("" if is_non_edited else " ещё"),
        callback_data="more-edit"
    ))
    edit_dailer_keyboard.row(InlineKeyboardButton(text="Сбросить редактированное", callback_data="drop-edited-edit"))
    edit_dailer_keyboard.row(InlineKeyboardButton(text="Сбросить все", callback_data="drop-edit"))
    
    edit_dailer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    return edit_dailer_keyboard

def classes_beginning_dailer():
    classes_beginning_dailer_keyboard = InlineKeyboardMarkup()
    
    # Year, month, day are filled with nonsense. The 1st classes start time is 8:00 am
    begin_time = datetime(1, 1, 1, hour=8, minute=0)
    
    for class_number in range(1, 4):
        classes_beginning_dailer_keyboard.row(InlineKeyboardButton(
            text=begin_time.strftime("%H:%M"),
            callback_data="edit-begin-time-{}".format(begin_time.strftime("%H:%M"))
        ))
        begin_time = begin_time + timedelta(hours=1, minutes=40)  # 1h 30m is class time, 10m is break time
    
    begin_time = begin_time + timedelta(minutes=30)  # There is a 40 minute break in the university
    
    for class_number in range(1, 5):
        classes_beginning_dailer_keyboard.row(InlineKeyboardButton(
            text=begin_time.strftime("%H:%M"),
            callback_data="edit-begin-time-{}".format(begin_time.strftime("%H:%M"))
            # Casting to integer to get rid of 0s in 08-like hours
        ))
        begin_time = begin_time + timedelta(hours=1, minutes=40)  # 1h 30m is class time, 10m is break time
    
    return classes_beginning_dailer_keyboard

def buildings_dailer():
    buildings_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dailer_keyboard.add(*[
        InlineKeyboardButton(text=building, callback_data="edit-building-{}".format(building)) for building in BUILDINGS
    ])

    return buildings_dailer_keyboard

def non_auditorium_chooser():
    non_auditorium_chooser_keyboard = InlineKeyboardMarkup()

    non_auditorium_chooser_keyboard.row(InlineKeyboardButton(text="кафедра", callback_data="каф"))
    non_auditorium_chooser_keyboard.row(InlineKeyboardButton(text="ВЦ", callback_data="вц"))

    return non_auditorium_chooser_keyboard
