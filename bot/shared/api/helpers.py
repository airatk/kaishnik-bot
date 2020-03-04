from bot.shared.api.types import SubjectScoreType
from bot.shared.api.subject import StudentSubject
from bot.shared.api.subject import LecturerSubject
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS
from bot.shared.calendar.week import is_even
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import DAYOFFS

from datetime import datetime
from datetime import timedelta


# Removes extraspaces & standardizing values to string type
def refine_raw_schedule(raw_schedule) -> [{str: str}]:
    return [ {
            key: " ".join(str(value).split()) for (key, value) in subject.items()
        } for subject in raw_schedule
    ]


def beautify_classes(raw_schedule: [{int: {str: str}}], is_next: bool, edited_subjects: [StudentSubject], settings: object) -> [str]:
    weekly_schedule: [str] = []
    
    today: datetime = datetime.today() + timedelta(days=7 if is_next else 0)
    today_weekday: int = today.isoweekday()
    is_asked_week_even = not is_even() if is_next else is_even()
    
    dayoffs: [(int, int)] = load_data(file=DAYOFFS)
    
    for weekday in WEEKDAYS:
        # Date of each weekday
        date: datetime = today + timedelta(days=weekday - today_weekday)
        
        # Finding out if the day is dayoff
        is_dayoff = (date.day, date.month) in dayoffs
        
        # Reseting `subjects_list` Adding the appropriate edited subjects to the schedule
        subjects_list: [(int, StudentSubject)] = [
            (subject.begin_hour, subject) for subject in edited_subjects if (
                subject.weekday == weekday and (subject.is_even is None or subject.is_even == is_asked_week_even)
            )
        ]
        
        if str(weekday) in raw_schedule and not is_dayoff:
            raw_schedule[str(weekday)] = refine_raw_schedule(raw_schedule[str(weekday)])
            
            for subject in raw_schedule[str(weekday)]:
                # No subjects - no schedule. For dayoffs
                if "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]: break
                
                # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
                if (subject["dayDate"] == "неч") if is_asked_week_even else (subject["dayDate"] == "чет"): continue
                
                # Do not show subjects with certain dates (21.09) on other dates (28 сентября) if asked
                if settings.are_classes_on_dates:
                    day_month = "{day}.{month}".format(day=int(date.strftime("%d")), month=date.strftime("%m"))
                    if "." in subject["dayDate"] and day_month not in subject["dayDate"]: continue
                
                studentSubject: StudentSubject = StudentSubject()
                
                studentSubject.time = (subject["dayTime"], subject["disciplType"])
                
                # Do not show subject if there is its edited alternative
                if studentSubject.begin_hour in [ begin_hour for (begin_hour, _) in subjects_list ]: continue
                
                studentSubject.building = subject["buildNum"]
                studentSubject.auditorium = subject["audNum"]
                studentSubject.dates = subject["dayDate"]
                studentSubject.title = subject["disciplName"]
                studentSubject.type = subject["disciplType"]
                studentSubject.lecturer = subject["prepodName"]
                studentSubject.department = subject["orgUnitName"]
                
                subjects_list.append((studentSubject.begin_hour, studentSubject))
            
        # Sort by begin_hour
        subjects_list.sort(key=lambda subject: subject[0])
        
        daily_schedule: str = "".join([ (subject.get() if settings.is_schedule_size_full else subject.get_compact()) for (_, subject) in subjects_list ])
        
        if daily_schedule == "":
            daily_schedule = "\n\nПраздничный выходной🥳" if is_dayoff else "\n\nВыходной"
        
        weekly_schedule.append("".join([
            "*{weekday}, {day} {month}*".format(weekday=WEEKDAYS[weekday], day=int(date.strftime("%d")), month=MONTHS[date.strftime("%m")]),
            daily_schedule
        ]))
    
    # Adding Sunday as well
    date: datetime = today + timedelta(days=7 - today.isoweekday())
    
    weekly_schedule.append("*Воскресенье, {day} {month}*\n\nОднозначно выходной".format(day=int(date.strftime("%d")), month=MONTHS[date.strftime("%m")]))
    
    return weekly_schedule

def beautify_exams(raw_schedule: [{int: {str: str}}]) -> str:
    raw_schedule = refine_raw_schedule(raw_schedule)
    
    schedule: str = ""
    
    for subject in raw_schedule:
        time_place: str = "\n\n*[ {date}, {time} ][ {building}, {auditorium} ]*".format(
            date=subject["examDate"], time=subject["examTime"],
            building=subject["buildNum"] + "ка", auditorium=subject["audNum"]
        )
        
        subject_name: str = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        lecturer: str = "\n@ {lecturer}".format(lecturer=subject["prepodName"].title()) if subject["prepodName"] else ""
        
        # Concatenate all the stuff above
        schedule = "".join([ schedule, time_place, subject_name, lecturer ])
    
    return schedule


def beautify_lecturers_classes(raw_schedule: [{int: {str: str}}], is_next: bool) -> [str]:
    weekly_schedule: [str] = []
    
    today: datetime = datetime.today() + timedelta(days=7 if is_next else 0)
    today_weekday: int = today.isoweekday()
    is_asked_week_even = not is_even() if is_next else is_even()
    
    for weekday in WEEKDAYS:
        # Date of each weekday
        date: datetime = today + timedelta(days=weekday - today_weekday)
        
        daily_schedule: str = ""
        previous_time: str = ""
        
        if str(weekday) not in raw_schedule:
            weekly_schedule.append("*{weekday}, {day} {month}*\n\nНет занятий".format(weekday=WEEKDAYS[weekday], day=int(date.strftime("%d")), month=MONTHS[date.strftime("%m")]))
            continue
        
        raw_schedule[str(weekday)] = refine_raw_schedule(raw_schedule[str(weekday)])
        
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        for subject in list(raw_schedule[str(weekday)]):
            if subject["dayDate"] == "неч" if is_asked_week_even else subject["dayDate"] == "чет":
                raw_schedule[str(weekday)].remove(subject)
        
        # Finnaly, setting subjects themselves
        for subject in raw_schedule[str(weekday)]:
            if previous_time == subject["dayTime"]: continue
            
            lecturerSubject: LecturerSubject = LecturerSubject()
            
            lecturerSubject.time = (subject["dayTime"], subject["disciplType"])
            lecturerSubject.building = subject["buildNum"]
            lecturerSubject.auditorium = subject["audNum"]
            lecturerSubject.dates = subject["dayDate"]
            lecturerSubject.title = subject["disciplName"]
            lecturerSubject.type = subject["disciplType"]
            
            previous_time = subject["dayTime"]
            
            for another_subject in raw_schedule[str(weekday)]:
                if previous_time == another_subject["dayTime"]:
                    lecturerSubject.groups.append(another_subject["group"])
            
            daily_schedule = "".join([ daily_schedule, lecturerSubject.get() ])
        
        weekly_schedule.append("".join([
            "*{weekday}, {day} {month}*".format(weekday=WEEKDAYS[weekday], day=int(date.strftime("%d")), month=MONTHS[date.strftime("%m")]),
            daily_schedule if daily_schedule != "" else "\n\nНет занятий"
        ]))
    
    return weekly_schedule

def beautify_lecturers_exams(raw_schedule: [{int: {str: str}}]) -> str:
    raw_schedule = refine_raw_schedule(raw_schedule)
    
    schedule: [(str, str)] = []
    
    for subject in raw_schedule:
        time_place: str = "\n\n*[ {date}, {time} ][ {building}, {auditorium} ]*".format(
            date=subject["examDate"], time=subject["examTime"],
            building=subject["buildNum"] + "ка", auditorium=subject["audNum"]
        )
        
        subject_name: str = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        group: str = "\n• У группы {group}".format(group=subject["group"])
        
        # To sort by date
        functional_date_entities: str = subject["examDate"].split(".")
        functional_date: str = "".join([ functional_date_entities[1], functional_date_entities[0] ])
        
        schedule.append((functional_date, "".join([ time_place, subject_name, group ])))
    
    schedule.sort(key=lambda subject: subject[0])
    
    return "".join([ subject for (_, subject) in schedule ])


def beautify_scoretable(raw_scoretable: [[str]]) -> [(str, str)]:
    scoretable: [(str, str)] = []
    
    for subject in raw_scoretable:
        unstyled_title: str = subject[1].replace("(экз.)", "").replace("(зач.)", "").replace("(зач./оц.)", "")
        title: str = "*{title}*".format(title=unstyled_title)
        
        if "(экз.)" in subject[1]: score_type: str = "".join([ "\n_", SubjectScoreType.EXAM.value, "_\n" ])
        elif "(зач.)" in subject[1]: score_type: str = "".join([ "\n_", SubjectScoreType.TEST.value, "_\n" ])
        elif "(зач./оц.)" in subject[1]: score_type: str = "".join([ "\n_", SubjectScoreType.GRADED_TEST.value, "_\n" ])
        else: score_type: str = "".join([ "\n_", SubjectScoreType.OTHER.value, "_\n" ])
        
        certification1: str = "\n• 1 аттестация: {gained} / {max}".format(gained=subject[2], max=subject[3])
        certification2: str = "\n• 2 аттестация: {gained} / {max}".format(gained=subject[4], max=subject[5])
        certification3: str = "\n• 3 аттестация: {gained} / {max}".format(gained=subject[6], max=subject[7])
        
        score_sum: str = "\n\n• За семестр: {gained} / {max}".format(
            gained=subject[8],
            max=(
                (int(subject[3]) if subject[3].isnumeric() else 0) +
                (int(subject[5]) if subject[5].isnumeric() else 0) +
                (int(subject[7]) if subject[7].isnumeric() else 0)
            )
        )
        debts: str = "\n• Долги: {}".format(subject[10])
        
        scoretable.append(
            (unstyled_title, "".join([ title, score_type, certification1, certification2, certification3, score_sum, debts ]))
        )
    
    return scoretable
