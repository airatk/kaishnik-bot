from typing import Dict
from typing import List

from vkwave.bots.utils.keyboards import Keyboard

from bot.platforms.vk.utilities.keyboards import menu_button

from bot.utilities.types import Commands
from bot.utilities.api.types import ScheduleType


def lecturer_chooser(names: List[Dict[str, str]]) -> str:
    lecturer_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    lecturer_chooser_keyboard.add_text_button(**menu_button())
    
    for name in names:
        lecturer_chooser_keyboard.add_row()
        lecturer_chooser_keyboard.add_text_button(text=name["lecturer"], payload={ 
            Commands.LECTURERS.value: "",
            "lecturer_id": name["id"]
        })
    
    return lecturer_chooser_keyboard.get_keyboard()

def lecturer_info_type_chooser(lecturer_id: str) -> str:
    lecturer_info_type_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    lecturer_info_type_chooser_keyboard.add_text_button(**menu_button())
    
    lecturer_info_type_chooser_keyboard.add_row()
    lecturer_info_type_chooser_keyboard.add_text_button(text="Занятия", payload={
        Commands.LECTURERS.value: "",
        ScheduleType.CLASSES.value: "",
        "lecturer_id": lecturer_id
    })

    lecturer_info_type_chooser_keyboard.add_row()
    lecturer_info_type_chooser_keyboard.add_text_button(text="Экзамены", payload={
        Commands.LECTURERS.value: "",
        ScheduleType.EXAMS.value: "", 
        "lecturer_id": lecturer_id
    })
    
    return lecturer_info_type_chooser_keyboard.get_keyboard()
