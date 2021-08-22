from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.utilities.types import Command


def semester_chooser(semesters_number: int) -> InlineKeyboardMarkup:
    semester_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    semester_chooser_keyboard.row(cancel_button())
    
    semester_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=str(semester),
            callback_data=" ".join([ Command.SCORE_SEMESTER.value, str(semester) ])
        ) for semester in range(1, semesters_number + 1)
    ])
    
    return semester_chooser_keyboard

def subjects_type_chooser(has_exams: bool, has_tests: bool, has_courseworks: bool) -> InlineKeyboardMarkup:
    subjects_type_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if any([ has_exams, has_courseworks, has_tests ]):
        subjects_type_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(
                text="показать все", callback_data=Command.SCORE_ALL.value
            )
        )
    
    if has_exams:
        subjects_type_chooser_keyboard.row(InlineKeyboardButton(
            text="экзамены", callback_data=Command.SCORE_EXAMS.value
        ))
    if has_courseworks:
        subjects_type_chooser_keyboard.row(InlineKeyboardButton(
            text="курсовые работы", callback_data=Command.SCORE_COURSEWORKS.value
        ))
    if has_tests:
        subjects_type_chooser_keyboard.row(InlineKeyboardButton(
            text="зачёты", callback_data=Command.SCORE_TESTS.value
        ))
    
    return subjects_type_chooser_keyboard

def subject_chooser(subjects: List[str], subject_type: str) -> InlineKeyboardMarkup:
    subject_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    subject_chooser_keyboard.row(
        cancel_button(),
        InlineKeyboardButton(
            text="показать все",
            callback_data=" ".join([ subject_type, "-" ])
        )
    )
    
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=title, callback_data=" ".join([ subject_type, str(index) ])
        ) for (index, title) in enumerate(subjects)
    ])
    
    return subject_chooser_keyboard
