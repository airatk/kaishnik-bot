from typing import List

from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.keyboards import menu_button

from bot.utilities.types import Command


def semester_chooser(semesters: List[str]) -> str:
    semester_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    semester_chooser_keyboard.add_text_button(**menu_button())
    
    for (index, semester) in enumerate(semesters):
        if index % 2 == 0:
            semester_chooser_keyboard.add_row()
        
        semester_chooser_keyboard.add_text_button(
            text=semester,
            payload={ Command.SCORE_SEMESTER.value: semester }
        )
    
    return semester_chooser_keyboard.get_keyboard()

def subject_chooser(subjects: List[str]) -> str:
    subject_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    subject_chooser_keyboard.add_text_button(**menu_button())
    subject_chooser_keyboard.add_text_button(
        text="Показать все",
        color=ButtonColor.SECONDARY,
        payload={ Command.SCORE_SUBJECT.value: "-" }
    )
    
    for (index, title) in enumerate(subjects):
        subject_chooser_keyboard.add_row()
        subject_chooser_keyboard.add_text_button(
            text=title if len(title) < 35 else f"{title[:35]}…",
            payload={ Command.SCORE_SUBJECT.value: str(index) }
        )
    
    return subject_chooser_keyboard.get_keyboard()
