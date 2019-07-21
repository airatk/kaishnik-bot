from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import MAX_CLASSES_NUMBER
from bot.helpers.constants import BUILDINGS

from datetime import datetime
from datetime import timedelta


def weektype_dialer():
    weektype_dialer_keyboard = InlineKeyboardMarkup()
    
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="чётная", callback_data="edit-weektype-even"))
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="нечётная", callback_data="edit-weektype-odd"))
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="каждая", callback_data="edit-weektype-none"))
    
    return weektype_dialer_keyboard

def weekday_dialer():
    weekday_dialer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    weekday_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    weekday_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=weekday_name,
            callback_data="edit-weekday-{}".format(weekday_number)
        ) for weekday_number, weekday_name in WEEKDAYS.items()
    ])
    
    return weekday_dialer_keyboard

def hours_dialer():
    hours_dialer_keyboard = InlineKeyboardMarkup()
    
    hours_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    time = datetime(1, 1, 1, hour=8, minute=0)  # An educational day starts at 8:00 am
    
    for class_number in range(MAX_CLASSES_NUMBER):
        hours_dialer_keyboard.row(
            InlineKeyboardButton(
                text=time.strftime("%H:%M"),
                callback_data="edit-time-{}".format(time.strftime("%H:%M"))
            )
        )
        
        time += timedelta(hours=1, minutes=40) + timedelta(minutes=30 if class_number == 2 else 0)
        # The length of a class is 1h 30m, the length of break is 10m, and there is 40m long break after the 3rd class
    
    return hours_dialer_keyboard

def buildings_dialer():
    buildings_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    buildings_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=building,
            callback_data="edit-building-{}".format(building)
        ) for building in BUILDINGS
    ])
    
    return buildings_dialer_keyboard

def subject_type_dialer():
    subject_type_dialer_keyboard = InlineKeyboardMarkup()
    
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="лекция", callback_data="edit-subject-type-лек"))
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="практика", callback_data="edit-subject-type-пр"))
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="ЛР", callback_data="edit-subject-type-л.р."))
    
    return subject_type_dialer_keyboard
