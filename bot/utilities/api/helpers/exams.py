from typing import Dict
from typing import List

from bot.utilities.api.constants import FULL_EXAM_ENTITIES
from bot.utilities.api.constants import COMPACT_EXAM_ENTITIES
from bot.utilities.api.constants import LECTURER_ENTITY
from bot.utilities.api.constants import GROUPS_ENTITY


def style_raw_student_exam(raw_exam: Dict[str, str], is_schedule_size_full: bool) -> str:
    styled_student_exam_entities: List[str] = [ style_raw_exam(
        raw_exam=raw_exam,
        is_schedule_size_full=is_schedule_size_full
    ) ]
    
    if raw_exam["prepodName"] != "" and is_schedule_size_full:
        styled_student_exam_entities.append(LECTURER_ENTITY.format(lecturer=raw_exam["prepodName"].title()))
    
    return "\n".join(styled_student_exam_entities)

def style_raw_lecturer_exam(raw_exam: Dict[str, str], is_schedule_size_full: bool) -> str:
    styled_lecturer_exam_entities: List[str] = [ 
        style_raw_exam(
            raw_exam=raw_exam,
            is_schedule_size_full=is_schedule_size_full
        )
    ]
    
    styled_lecturer_exam_entities.append(GROUPS_ENTITY.format(group=raw_exam["group"]))
    
    return "\n".join(styled_lecturer_exam_entities)


def style_raw_exam(raw_exam: Dict[str, str], is_schedule_size_full: bool) -> str:
    styled_exam_entities: List[str] = list(FULL_EXAM_ENTITIES if is_schedule_size_full else COMPACT_EXAM_ENTITIES)
    
    styled_exam_template: str = "\n".join(styled_exam_entities)
    
    styled_exam_filling: str = {
        "date": raw_exam["examDate"],
        "time": raw_exam["examTime"],
        "building": raw_exam["buildNum"],
        "auditorium": raw_exam["audNum"],
        "title": raw_exam["disciplName"]
    }
    
    return styled_exam_template.format(**styled_exam_filling)
