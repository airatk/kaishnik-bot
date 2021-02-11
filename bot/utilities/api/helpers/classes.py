from datetime import datetime
from datetime import timedelta

from typing import Dict
from typing import List

from bot.utilities.api.constants import FULL_CLASS_ENTITIES
from bot.utilities.api.constants import COMPACT_CLASS_ENTITIES
from bot.utilities.api.constants import LECTURER_ENTITY
from bot.utilities.api.constants import DEPARTMENT_ENTITY
from bot.utilities.api.constants import GROUPS_ENTITY
from bot.utilities.api.types import ClassType


def style_raw_student_class(raw_class: Dict[str, str], is_schedule_size_full: bool, should_show_entire_semester: bool) -> str:
    styled_student_class_entities: List[str] = [ style_raw_class(
        raw_class=raw_class,
        is_schedule_size_full=is_schedule_size_full,
        should_show_entire_semester=should_show_entire_semester
    ) ]
    
    if raw_class["prepodName"] != "" and is_schedule_size_full:
        styled_student_class_entities.append(LECTURER_ENTITY.format(lecturer=raw_class["prepodName"].title()))
    
    if raw_class["orgUnitName"] != "" and is_schedule_size_full:
        styled_student_class_entities.append(DEPARTMENT_ENTITY.format(department=raw_class["orgUnitName"]))
    
    return "\n".join(styled_student_class_entities)

def style_raw_lecturer_class(raw_class: Dict[str, str], is_schedule_size_full: bool, should_show_entire_semester: bool, groups: List[str]) -> str:
    styled_lecturer_class_entities: List[str] = [ style_raw_class(
        raw_class=raw_class,
        is_schedule_size_full=is_schedule_size_full,
        should_show_entire_semester=should_show_entire_semester
    ) ]
    
    styled_lecturer_class_entities.append("\n".join([ GROUPS_ENTITY.format(group=group) for group in groups ]))
    
    return "\n".join(styled_lecturer_class_entities)


def style_raw_class(raw_class: Dict[str, str], is_schedule_size_full: bool, should_show_entire_semester: bool) -> str:
    styled_class_entities: List[str] = list(FULL_CLASS_ENTITIES if is_schedule_size_full else COMPACT_CLASS_ENTITIES)
    
    # Removing 'dates' from template if there is no dates
    if raw_class["dayDate"] == "" or not any([
        should_show_entire_semester,
        "." in raw_class["dayDate"],
        "/" in raw_class["dayDate"],
        "(" in raw_class["dayDate"]
    ]): del styled_class_entities[1]
    
    styled_class_template: str = "\n".join(styled_class_entities)
    
    if "Военная подготовка" in raw_class["disciplName"]:
        raw_class["disciplType"] = ClassType.MILITARY_TRAINING.value

    styled_class_filling: str = {
        "time": refine_class_time(raw_time=raw_class["dayTime"], raw_type=raw_class["disciplType"]),
        "place": refine_class_place(raw_building=raw_class["buildNum"], raw_auditorium=raw_class["audNum"]),
        "dates": refine_class_dates(raw_dates=raw_class["dayDate"]),
        "title": raw_class["disciplName"],
        "type": refine_class_type(
            raw_type=raw_class["disciplType"],
            is_multigroup=(raw_class.get("potok", "") != ""),
            is_schedule_size_full=is_schedule_size_full
        )
    }
    
    return styled_class_template.format(**styled_class_filling)


def refine_class_time(raw_time: str, raw_type: str) -> str:
    (hours, minutes) = map(int, raw_time.split(":"))
    start_time: datetime = datetime(1, 1, 1, hours, minutes)  # Year, month, day are filled with nonsence
    duration: timedelta = timedelta(hours=1, minutes=30)  # Class duration is 1.5h
    
    if raw_type == ClassType.MILITARY_TRAINING.value:
        start_time = datetime(1, 1, 1, 7, 50)
        # Military training classes start 10 minutes earlier than the usual ones

        duration = timedelta(hours=9, minutes=10)
        # Military training classes last all day
    elif raw_type == ClassType.LAB.value:
        duration = timedelta(hours=3, minutes=40 if start_time.hour == 11 else 10)
        # Lab duration is 3h with a 40/10m long break
    
    end_time: datetime = start_time + duration
    
    return " - ".join([ start_time.strftime("%H:%M"), end_time.strftime("%H:%M") ])

def refine_class_place(raw_building: str, raw_auditorium: str) -> str:
    if "ОЛИМП" in raw_building.upper(): return "СК Олимп"
    if "-----" in raw_building.upper(): return "ВУЦ"
    
    return "".join([ raw_building, "ка", "".join([ ", ", raw_auditorium ]) if raw_auditorium != "" else "" ])

def refine_class_dates(raw_dates: str) -> str:
    raw_dates = raw_dates.replace("чет", "чётная")
    raw_dates = raw_dates.replace("неч", "нечётная")
    
    return raw_dates

def refine_class_type(raw_type: str, is_multigroup: bool, is_schedule_size_full: bool) -> str:
    class_type: str = ""
    
    if raw_type == ClassType.LECTURE.value:
        class_type = "лекция" if is_schedule_size_full else "Л"
    elif raw_type == ClassType.PRACTICE.value:
        class_type = "практика" if is_schedule_size_full else "П"
    elif raw_type == ClassType.LAB.value:
        class_type = "лабораторная работа" if is_schedule_size_full else "ЛР"
    elif raw_type == ClassType.CONSULTATION.value:
        class_type = "консультация" if is_schedule_size_full else "К"
    elif raw_type == ClassType.MILITARY_TRAINING.value:
        class_type = "согласно расписанию ВУЦ" if is_schedule_size_full else "С"
        is_multigroup = False
    else:
        class_type = raw_type
    
    if is_multigroup:
        class_type = " ".join([ class_type, "(потоковая)" if is_schedule_size_full else "(п)" ])
    
    return class_type
