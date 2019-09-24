from telebot.types import InlineKeyboardButton

from bot.commands.edit.utilities.constants import MAX_CLASSES_NUMBER

from bot.commands.locations.utilities.constants import BUILDINGS

from bot.shared.keyboards import cancel_option
from bot.shared.api.subject import SubjectType
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekParity
from bot.shared.commands import Commands

from datetime import datetime
from datetime import timedelta


def action_chooser(has_edits):
    action_chooser_keyboard = cancel_option()
    
    action_chooser_keyboard.row(InlineKeyboardButton(text="изменить", callback_data=Commands.EDIT_ADD.value))
    
    if has_edits:
        action_chooser_keyboard.row(InlineKeyboardButton(text="показать", callback_data=Commands.EDIT_SHOW.value))
        action_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data=Commands.EDIT_DELETE.value))
    
    return action_chooser_keyboard


def skip(ACTION):
    skip_keyboard = cancel_option()
    
    skip_keyboard.row(InlineKeyboardButton(text="пропустить", callback_data=ACTION.value))
    
    return skip_keyboard

def weektype_editer():
    weektype_editer_keyboard = cancel_option()
    
    weektype_editer_keyboard.row(InlineKeyboardButton(text="каждая", callback_data=" ".join([
        Commands.EDIT_WEEKTYPE.value, WeekParity.BOTH.value
    ])))
    weektype_editer_keyboard.row(InlineKeyboardButton(text="чётная", callback_data=" ".join([
        Commands.EDIT_WEEKTYPE.value, WeekParity.EVEN.value
    ])))
    weektype_editer_keyboard.row(InlineKeyboardButton(text="нечётная", callback_data=" ".join([
        Commands.EDIT_WEEKTYPE.value, WeekParity.ODD.value
    ])))
    
    return weektype_editer_keyboard

def weekday_editer():
    weekday_editer_keyboard = cancel_option()
    
    weekday_editer_keyboard.add(*[
        InlineKeyboardButton(
            text=weekday_name, callback_data=" ".join([ Commands.EDIT_WEEKDAY.value, str(weekday_number) ])
        ) for (weekday_number, weekday_name) in WEEKDAYS.items()
    ])
    
    return weekday_editer_keyboard

def hours_editer():
    hours_editer_keyboard = cancel_option()
    
    time = datetime(1, 1, 1, hour=8, minute=0)  # An educational day starts at 8:00 am
    
    for class_number in range(MAX_CLASSES_NUMBER):
        hours_editer_keyboard.row(InlineKeyboardButton(
            text=time.strftime("%H:%M"), callback_data=" ".join([ Commands.EDIT_TIME.value, time.strftime("%H:%M") ])
        ))
        
        # The length of a class is 1h 30m, the length of a break is 10m, and there is 40m long break after the 3rd class
        time += timedelta(hours=1, minutes=40) + timedelta(minutes=30 if class_number == 2 else 0)
    
    return hours_editer_keyboard

def buildings_editer():
    buildings_editer_keyboard = cancel_option(row_width=4)
    
    buildings_editer_keyboard.add(*[
        InlineKeyboardButton(
            text=building, callback_data=" ".join([ Commands.EDIT_BUILDING.value, building ])
        ) for building in BUILDINGS
    ])
    
    return buildings_editer_keyboard

def subject_type_editer():
    subject_type_editer_keyboard = cancel_option()
    
    subject_type_editer_keyboard.row(InlineKeyboardButton(text="лекция", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, SubjectType.LECTURE.value
    ])))
    subject_type_editer_keyboard.row(InlineKeyboardButton(text="практика", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, SubjectType.PRACTICE.value
    ])))
    subject_type_editer_keyboard.row(InlineKeyboardButton(text="лабораторная работа", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, SubjectType.LAB.value
    ])))
    subject_type_editer_keyboard.row(InlineKeyboardButton(text="консультация", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, SubjectType.CONSULTATION.value
    ])))
    
    return subject_type_editer_keyboard


def weektype_chooser(classes_on_both, classes_on_even, classes_on_odd, ACTION):
    weektype_chooser_keyboard = cancel_option()
    
    if classes_on_both + classes_on_even + classes_on_odd > 1:
        if ACTION is Commands.EDIT_SHOW_WEEKTYPE:
            action = "показать все"
            callback_action = Commands.EDIT_SHOW_ALL.value
        elif ACTION is Commands.EDIT_DELETE_WEEKTYPE:
            action = "удалить все"
            callback_action = Commands.EDIT_DELETE_ALL.value
        
        weektype_chooser_keyboard.row(InlineKeyboardButton(text=action, callback_data=callback_action))
    
    if classes_on_both != 0:
        weektype_chooser_keyboard.row(InlineKeyboardButton(
            text="каждая ({edits_number})".format(edits_number=classes_on_both),
            callback_data=" ".join([ ACTION.value, WeekParity.BOTH.value ])
        ))
    if classes_on_even != 0:
        weektype_chooser_keyboard.row(InlineKeyboardButton(
            text="чётная ({edits_number})".format(edits_number=classes_on_even),
            callback_data=" ".join([ ACTION.value, WeekParity.EVEN.value ])
        ))
    if classes_on_odd != 0:
        weektype_chooser_keyboard.row(InlineKeyboardButton(
            text="нечётная ({edits_number})".format(edits_number=classes_on_odd),
            callback_data=" ".join([ ACTION.value, WeekParity.ODD.value ])
        ))
    
    return weektype_chooser_keyboard

def weekday_chooser(weektype, subjects_number_by_weekdays, ACTION):
    weekday_chooser_keyboard = cancel_option()
    
    if sum(subjects_number_by_weekdays) > 1:
        if ACTION is Commands.EDIT_SHOW_WEEKDAY:
            action = "Показать все"
            callback_action = Commands.EDIT_SHOW_ALL.value
        elif ACTION is Commands.EDIT_DELETE_WEEKDAY:
            action = "Удалить все"
            callback_action = Commands.EDIT_DELETE_ALL.value
        
        weekday_chooser_keyboard.row(InlineKeyboardButton(text=action, callback_data=" ".join([
            callback_action, weektype
        ])))
    
    weekday_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text="{weekday_name} ({edits_number})".format(
                weekday_name=weekday_name, edits_number=subjects_number_by_weekdays[weekday - 1]
            ),
            callback_data=" ".join([ ACTION.value, weektype, str(weekday) ])
        ) for (weekday, weekday_name) in WEEKDAYS.items() if subjects_number_by_weekdays[weekday - 1] != 0
    ])
    
    return weekday_chooser_keyboard

def edit_chooser(weektype, weekday, subjects, ACTION):
    edit_chooser_keyboard = cancel_option()
    
    if len(subjects) > 1:
        if ACTION is Commands.EDIT_SHOW_EDIT:
            action = "Показать все"
            callback_action = Commands.EDIT_SHOW_ALL.value
        elif ACTION is Commands.EDIT_DELETE_EDIT:
            action = "Удалить все"
            callback_action = Commands.EDIT_DELETE_ALL.value
        
        edit_chooser_keyboard.row(InlineKeyboardButton(text=action, callback_data=" ".join([
            callback_action, weektype, weekday
        ])))
    
    edit_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject.get_simple(), callback_data=" ".join([ ACTION.value, str(index) ])
        ) for (index, subject) in subjects.items()
    ])
    
    return edit_chooser_keyboard
