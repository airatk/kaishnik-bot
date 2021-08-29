from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.utilities.types import Command


def semester_chooser(semesters: List[str]) -> InlineKeyboardMarkup:
    semester_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    semester_chooser_keyboard.row(cancel_button())
    
    semester_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=semester,
            callback_data=" ".join([ Command.SCORE_SEMESTER.value, semester ])
        ) for semester in semesters
    ])
    
    return semester_chooser_keyboard

def subject_chooser(subjects: List[str]) -> InlineKeyboardMarkup:
    subject_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    subject_chooser_keyboard.row(
        cancel_button(),
        InlineKeyboardButton(
            text="показать все", 
            callback_data=" ".join([ Command.SCORE_SUBJECT.value, "-" ])
        )
    )
    
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=title, 
            callback_data=" ".join([ Command.SCORE_SUBJECT.value, str(index) ])
        ) for (index, title) in enumerate(subjects)
    ])
    
    return subject_chooser_keyboard
