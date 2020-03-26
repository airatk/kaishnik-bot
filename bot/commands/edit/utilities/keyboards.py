from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.commands.locations.utilities.constants import BUILDINGS

from bot.shared.keyboards import cancel_button
from bot.shared.api.subject import StudentSubject
from bot.shared.api.subject import Subject
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekParity
from bot.shared.commands import Commands


def action_chooser(has_edits: bool) -> InlineKeyboardMarkup:
    action_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    action_chooser_keyboard.row(cancel_button())
    
    action_chooser_keyboard.row(InlineKeyboardButton(text="изменить", callback_data=Commands.EDIT_ADD.value))
    
    if has_edits:
        action_chooser_keyboard.row(InlineKeyboardButton(text="показать", callback_data=Commands.EDIT_SHOW.value))
        action_chooser_keyboard.row(InlineKeyboardButton(text="удалить", callback_data=Commands.EDIT_DELETE.value))
    
    return action_chooser_keyboard


def skip(ACTION: Commands) -> InlineKeyboardMarkup:
    skip_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    skip_keyboard.add(*[
        cancel_button(),
        InlineKeyboardButton(text="пропустить", callback_data=ACTION.value)
    ])
    
    return skip_keyboard


def weektype_editor() -> InlineKeyboardMarkup:
    weektype_editor_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    weektype_editor_keyboard.row(cancel_button())
    
    weektype_editor_keyboard.row(InlineKeyboardButton(text="каждая", callback_data=" ".join([
        Commands.EDIT_WEEKTYPE.value, WeekParity.BOTH.value
    ])))
    weektype_editor_keyboard.row(InlineKeyboardButton(text="чётная", callback_data=" ".join([
        Commands.EDIT_WEEKTYPE.value, WeekParity.EVEN.value
    ])))
    weektype_editor_keyboard.row(InlineKeyboardButton(text="нечётная", callback_data=" ".join([
        Commands.EDIT_WEEKTYPE.value, WeekParity.ODD.value
    ])))
    
    return weektype_editor_keyboard

def weekday_editor() -> InlineKeyboardMarkup:
    weekday_editor_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    weekday_editor_keyboard.row(cancel_button())
    
    weekday_editor_keyboard.add(*[
        InlineKeyboardButton(
            text=weekday_name, callback_data=" ".join([ Commands.EDIT_WEEKDAY.value, str(weekday_number) ])
        ) for (weekday_number, weekday_name) in WEEKDAYS.items()
    ])
    
    return weekday_editor_keyboard

def hour_editor() -> InlineKeyboardMarkup:
    hour_editor_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    hour_editor_keyboard.row(cancel_button())
    
    hour_editor_keyboard.add(*[
        InlineKeyboardButton(
            text="{:0=2d}:xx".format(hour),
            callback_data=" ".join([ Commands.EDIT_HOUR.value, "{:0=2d}:xx".format(hour) ])
        ) for hour in range(6, 24)  # The working hours of the univeristy
    ])
    
    return hour_editor_keyboard

def time_editor(hour: int) -> InlineKeyboardMarkup:
    time_editor_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    time_editor_keyboard.row(cancel_button())
    
    time_editor_keyboard.add(*[
        InlineKeyboardButton(
            text="{:0=2d}:{:0=2d}".format(hour, minute),
            callback_data=" ".join([ Commands.EDIT_TIME.value, "{:0=2d}:{:0=2d}".format(hour, minute) ])
        ) for minute in range(0, 60, 5)  # Iterating every 5 minutes within an hour
    ])
    
    return time_editor_keyboard

def buildings_editor() -> InlineKeyboardMarkup:
    buildings_editor_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=4)
    
    buildings_editor_keyboard.row(cancel_button())
    
    buildings_editor_keyboard.add(*[
        InlineKeyboardButton(
            text=building, callback_data=" ".join([ Commands.EDIT_BUILDING.value, building ])
        ) for building in BUILDINGS
    ])
    
    return buildings_editor_keyboard

def subject_type_editor() -> InlineKeyboardMarkup:
    subject_type_editor_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    subject_type_editor_keyboard.row(cancel_button())
    
    subject_type_editor_keyboard.row(InlineKeyboardButton(text="лекция", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, Subject.Type.LECTURE.value
    ])))
    subject_type_editor_keyboard.row(InlineKeyboardButton(text="практика", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, Subject.Type.PRACTICE.value
    ])))
    subject_type_editor_keyboard.row(InlineKeyboardButton(text="лабораторная работа", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, Subject.Type.LAB.value
    ])))
    subject_type_editor_keyboard.row(InlineKeyboardButton(text="консультация", callback_data=" ".join([
        Commands.EDIT_SUBJECT_TYPE.value, Subject.Type.CONSULTATION.value
    ])))
    
    return subject_type_editor_keyboard


def weektype_chooser(classes_on_both: int, classes_on_even: int, classes_on_odd: int, ACTION: Commands) -> InlineKeyboardMarkup:
    weektype_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if classes_on_both + classes_on_even + classes_on_odd > 1:
        if ACTION is Commands.EDIT_SHOW_WEEKTYPE:
            (action, callback_action) = ("показать все", Commands.EDIT_SHOW_ALL.value)
        elif ACTION is Commands.EDIT_DELETE_WEEKTYPE:
            (action, callback_action) = ("удалить все", Commands.EDIT_DELETE_ALL.value)
        
        weektype_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(text=action, callback_data=callback_action)
        )
    else:
        weektype_chooser_keyboard.row(cancel_button())
    
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

def weekday_chooser(weektype: str, subjects_number_by_weekdays: [int], ACTION: Commands) -> InlineKeyboardMarkup:
    weekday_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if sum(subjects_number_by_weekdays) > 1:
        if ACTION is Commands.EDIT_SHOW_WEEKDAY:
            (action, callback_action) = ("показать все", Commands.EDIT_SHOW_ALL.value)
        elif ACTION is Commands.EDIT_DELETE_WEEKDAY:
            (action, callback_action) = ("удалить все", Commands.EDIT_DELETE_ALL.value)
        
        weekday_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(text=action, callback_data=" ".join([ callback_action, weektype ]))
        )
    else:
        weekday_chooser_keyboard.row(cancel_button())
    
    weekday_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text="{weekday_name} ({edits_number})".format(
                weekday_name=weekday_name,
                edits_number=subjects_number_by_weekdays[weekday - 1]
            ),
            callback_data=" ".join([ ACTION.value, weektype, str(weekday) ])
        ) for (weekday, weekday_name) in WEEKDAYS.items() if subjects_number_by_weekdays[weekday - 1] != 0
    ])
    
    return weekday_chooser_keyboard

def edit_chooser(weektype: str, weekday: int, subjects: [StudentSubject], ACTION: Commands) -> InlineKeyboardMarkup:
    edit_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if len(subjects) > 1:
        if ACTION is Commands.EDIT_SHOW_EDIT:
            (action, callback_action) = ("показать все", Commands.EDIT_SHOW_ALL.value)
        elif ACTION is Commands.EDIT_DELETE_EDIT:
            (action, callback_action) = ("удалить все", Commands.EDIT_DELETE_ALL.value)
        
        edit_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(text=action, callback_data=" ".join([ callback_action, weektype, weekday ]))
        )
    else:
        edit_chooser_keyboard.row(cancel_button())
    
    edit_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject.get_simple(), callback_data=" ".join([ ACTION.value, str(index) ])
        ) for (index, subject) in subjects.items()
    ])
    
    return edit_chooser_keyboard
