from datetime import datetime

from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional

from bot.models.settings import Settings
from bot.models.day_off import DayOff

from bot.utilities.api.helpers.classes import style_raw_student_class
from bot.utilities.api.helpers.classes import style_raw_lecturer_class
from bot.utilities.api.helpers.exams import style_raw_student_exam
from bot.utilities.api.helpers.exams import style_raw_lecturer_exam
from bot.utilities.calendar.constants import WEEKDAYS
from bot.utilities.calendar.constants import MONTHS
from bot.utilities.calendar.helpers import is_week_even


# Removes extra spaces & standardising values to string type
def refine_raw_schedule(raw_schedule: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    return list(map(lambda raw_class: { key: " ".join(str(value).split()) for (key, value) in raw_class.items() }, raw_schedule))


def beautify_classes(raw_schedule: Dict[str, List[Dict[str, str]]], settings: Settings, dates: List[str] = []) -> List[str]:
    should_show_entire_semester: bool = (len(dates) == 0)
    
    dates = list(WEEKDAYS.keys()) if should_show_entire_semester else sorted(
        dates, key=lambda raw_date: datetime(year=datetime.today().year, month=int(raw_date[3:5]), day=int(raw_date[0:2]))
    )
    
    beautified_classes: List[str] = []
    
    for raw_date in dates:
        if not should_show_entire_semester:
            (raw_day, raw_month) = raw_date.split(".")
            day_date: Optional[datetime] = datetime(datetime.today().year, int(raw_month), int(raw_day))
            
            is_day_off: bool = DayOff.select().where(DayOff.day == day_date.strftime("%d-%m")).exists()
            
            weekday: str = str(day_date.isoweekday())
        else:
            (raw_day, raw_month) = (None, None)
            day_date: Optional[datetime] = None

            is_day_off: bool = False

            weekday: str = str(raw_date)
        
        # Resetting the list
        classes_list: List[Tuple[int, str]] = []
        
        if weekday in raw_schedule and (should_show_entire_semester or not is_day_off):
            raw_schedule[weekday] = refine_raw_schedule(raw_schedule[weekday])
            
            for raw_class in raw_schedule[weekday]:
                # No classes - no schedule. For days off
                if "День консультаций" in raw_class["disciplName"]: break
                
                # Removing extra whitespaces from dates
                raw_class["dayDate"] = raw_class["dayDate"].replace(" ", "").replace(",", ", ")
                
                if not should_show_entire_semester:
                    # Do not show classes on even weeks when they are supposed to be on odd weeks
                    if (raw_class["dayDate"] == "неч") if is_week_even(day_date) else (raw_class["dayDate"] == "чет"): continue
                    
                    # Do not show classes with certain dates (21.09) on other dates (28 сентября)
                    if "." in raw_class["dayDate"] and (
                        "{day}.{month}".format(day=int(raw_day), month=raw_month) not in raw_class["dayDate"] and
                        raw_date not in raw_class["dayDate"]
                    ): continue
                
                class_start_hour: str = raw_class["dayTime"].split(":")[0]
                
                styled_class: str = style_raw_student_class(
                    raw_class=raw_class,
                    is_schedule_size_full=settings.is_schedule_size_full,
                    should_show_entire_semester=should_show_entire_semester
                )
                
                classes_list.append((class_start_hour, styled_class))
        
        # Sort by begin_hour
        classes_list.sort(key=lambda hour_and_class: hour_and_class[0])
        
        classes: str = "\n\n".join([ styled_class for (_, styled_class) in classes_list ])
        
        if classes == "":
            if not should_show_entire_semester and is_day_off:
                classes = DayOff.get(DayOff.day == day_date.strftime("%d-%m")).message
            else:
                classes = "Выходной"
        
        if should_show_entire_semester:
            classes_day: str = "*{weekday}*".format(weekday=WEEKDAYS[int(weekday)])
        else:
            classes_day: str = "*{weekday}, {day} {month}*".format(
                weekday=WEEKDAYS.get(int(weekday), "Воскресенье"),
                day=int(raw_day), month=MONTHS[raw_month]
            )
        
        beautified_classes.append("\n\n".join([ classes_day, classes ]))
    
    return beautified_classes

def beautify_exams(raw_schedule: Dict[str, List[Dict[str, str]]], settings: Settings) -> str:
    raw_schedule: List[Dict[str, str]] = refine_raw_schedule(raw_schedule=raw_schedule)
    
    raw_schedule.sort(key=lambda raw_exam: ".".join(raw_exam["examDate"].split(".")[:2][::-1]))
    
    exams_list: List[str] = [ 
        style_raw_student_exam(
            raw_exam=raw_exam,
            is_schedule_size_full=settings.is_schedule_size_full
        ) for raw_exam in raw_schedule 
    ]
    
    return "\n\n".join(exams_list)


def beautify_lecturers_classes(raw_schedule: Dict[str, List[Dict[str, str]]], settings: Settings, dates: List[str] = []) -> List[str]:
    should_show_entire_semester: bool = (len(dates) == 0)

    dates = list(WEEKDAYS.keys()) if should_show_entire_semester else sorted(
        dates, key=lambda raw_date: datetime(datetime.today().year, int(raw_date[3:5]), int(raw_date[0:2]))
    )
    
    initial_raw_schedule: Dict[str, List[Dict[str, str]]] = raw_schedule
    beautified_classes: List[str] = []
    
    for raw_date in dates:
        raw_schedule = dict(initial_raw_schedule)
        
        if not should_show_entire_semester:
            (raw_day, raw_month) = raw_date.split(".")
            day_date: datetime = datetime(datetime.today().year, int(raw_month), int(raw_day))
            
            weekday: str = str(day_date.isoweekday())
        else:
            (raw_day, raw_month) = (None, None)
            day_date: datetime = None
            
            weekday: str = str(raw_date)
        
        classes_list: List[Tuple[str, str]] = []
        
        previous_time: str = ""
        previous_date: str = ""
        
        if weekday not in raw_schedule:
            beautified_classes.append("*{weekday}*\n\nНет занятий".format(
                weekday=WEEKDAYS[int(weekday)]
            ) if should_show_entire_semester else "*{weekday}, {day} {month}*\n\nНет занятий".format(
                weekday=WEEKDAYS.get(int(weekday), "Воскресенье"),
                day=int(raw_day), month=MONTHS[raw_month])
            )
            continue
        
        raw_schedule[weekday] = refine_raw_schedule(raw_schedule[weekday])
        
        # Clearing extra whitespaces from dates
        for (raw_class_index, raw_class) in enumerate(raw_schedule[weekday]):
            raw_schedule[weekday][raw_class_index]["dayDate"] = raw_class["dayDate"].replace(" ", "").replace(",", ", ")
        
        if not should_show_entire_semester:
            for raw_class in list(raw_schedule[weekday]):
                # Do not show classes on even weeks when they are supposed to be on odd weeks if that's not asked
                if (raw_class["dayDate"] == "неч") if is_week_even(day_date) else (raw_class["dayDate"] == "чет"):
                    raw_schedule[weekday].remove(raw_class)
                
                if "." in raw_class["dayDate"] and (
                    "{day}.{month}".format(day=int(raw_day), month=raw_month) not in raw_class["dayDate"] and
                    raw_date not in raw_class["dayDate"]
                ):
                    raw_schedule[weekday].remove(raw_class)
        
        # Setting classes themselves
        for raw_class in raw_schedule[weekday]:
            class_groups: List[str] = []
            
            if previous_time == raw_class["dayTime"] and previous_date == raw_class["dayDate"]: continue
            
            previous_time = raw_class["dayTime"]
            previous_date = raw_class["dayDate"]
            
            for another_raw_class in raw_schedule[weekday]:
                if previous_time == another_raw_class["dayTime"] and previous_date == another_raw_class["dayDate"]:
                    class_groups.append(another_raw_class["group"])
            
            class_start_hour: str = raw_class["dayTime"].split(":")[0]
            
            styled_class: str = style_raw_lecturer_class(
                raw_class=raw_class,
                is_schedule_size_full=settings.is_schedule_size_full,
                should_show_entire_semester=should_show_entire_semester,
                groups=class_groups
            )
            
            classes_list.append((class_start_hour, styled_class))
        
        classes_list.sort(key=lambda hour_and_class: hour_and_class[0])
        
        classes: str = "\n\n".join([ styled_class for (_, styled_class) in classes_list ])
        
        if classes == "":
            classes = "Нет занятий"
        
        beautified_classes.append("\n\n".join([
            "*{weekday}*".format(
                weekday=WEEKDAYS[int(weekday)]
            ) if should_show_entire_semester else "*{weekday}, {day} {month}*".format(
                weekday=WEEKDAYS.get(int(weekday), "Воскресенье"),
                day=int(raw_day), month=MONTHS[raw_month]
            ),
            classes
        ]))
    
    return beautified_classes

def beautify_lecturers_exams(raw_schedule: Dict[str, List[Dict[str, str]]], settings: Settings) -> str:
    raw_schedule: List[Dict[str, str]] = refine_raw_schedule(raw_schedule=raw_schedule)
    
    raw_schedule.sort(key=lambda raw_exam: ".".join(raw_exam["examDate"].split(".")[:2][::-1]))
    
    exams_list: List[str] = [ 
        style_raw_lecturer_exam(
            raw_exam=raw_exam,
            is_schedule_size_full=settings.is_schedule_size_full
        ) for raw_exam in raw_schedule 
    ]
    
    return "\n\n".join(exams_list)
