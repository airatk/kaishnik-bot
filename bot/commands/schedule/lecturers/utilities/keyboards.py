from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.keyboards import cancel_button
from bot.shared.api.types import ScheduleType
from bot.shared.commands import Commands


def lecturer_chooser(names: [{str: str}]) -> InlineKeyboardMarkup:
    lecturer_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    lecturer_chooser_keyboard.row(cancel_button())
    
    lecturer_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=name["lecturer"], callback_data=" ".join([ Commands.LECTURERS.value, name["id"] ])
        ) for name in names
    ])
    
    return lecturer_chooser_keyboard

def lecturer_info_type_chooser(lecturer_id: str) -> InlineKeyboardMarkup:
    lecturer_info_type_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    lecturer_info_type_chooser_keyboard.row(cancel_button())
    
    lecturer_info_type_chooser_keyboard.add(
        InlineKeyboardButton(text="занятия", callback_data=" ".join([ ScheduleType.CLASSES.value, lecturer_id ])),
        InlineKeyboardButton(text="экзамены", callback_data=" ".join([ ScheduleType.EXAMS.value, lecturer_id ]))
    )
    
    return lecturer_info_type_chooser_keyboard
