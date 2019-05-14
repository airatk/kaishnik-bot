from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.constants import WEEKDAYS
from bot.constants import MAX_CLASSES_NUMBER
from bot.constants import BUILDINGS

from datetime import datetime
from datetime import timedelta


# /edit menu
def edit_chooser():
    edit_chooser_keyboard = InlineKeyboardMarkup()
    
    edit_chooser_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    edit_chooser_keyboard.row(InlineKeyboardButton(text="изменить", callback_data="add-edit"))
    edit_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data="delete-edit"))
    
    return edit_chooser_keyboard


# "edit" option
def weektype_dialer():
    weektype_dialer_keyboard = InlineKeyboardMarkup()
    
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="нечётная", callback_data="edit-weektype-odd"))
    weektype_dialer_keyboard.row(InlineKeyboardButton(text="чётная", callback_data="edit-weektype-even"))
    
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
    
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="практика", callback_data="edit-subject-type-пр"))
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="лекция", callback_data="edit-subject-type-лек"))
    subject_type_dialer_keyboard.row(InlineKeyboardButton(text="ЛР", callback_data="edit-subject-type-л.р."))
    
    return subject_type_dialer_keyboard


# "delete" option
def delete_edit_chooser(edited_subjects):
    delete_edit_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    delete_edit_chooser_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    delete_edit_chooser_keyboard.row(InlineKeyboardButton(text="удалить все", callback_data="delete-edit-all"))
    
    delete_edit_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject.get_simple(),
            callback_data="delete-edit-number-{}".format(index)
        ) for index, subject in enumerate(edited_subjects)
    ])
    
    return delete_edit_chooser_keyboard


# helpers
def edit_canceler():
    edit_canceler_keyboard = InlineKeyboardMarkup()
    
    edit_canceler_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    return edit_canceler_keyboard

def canceler_skipper(callback_data):
    canceler_skipper_keyboard = InlineKeyboardMarkup()
    
    canceler_skipper_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    canceler_skipper_keyboard.row(InlineKeyboardButton(text="пропустить", callback_data=callback_data))
    
    return canceler_skipper_keyboard
