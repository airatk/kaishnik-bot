from bot.shared.api.types import ScoreType
from bot.shared.api.subject import StudentSubject
from bot.shared.api.subject import LecturerSubject
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS
from bot.shared.calendar.helpers import is_week_even
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import DAYOFFS

from datetime import date


# Removes extra spaces & standardising values to string type
def refine_raw_schedule(raw_schedule) -> [{str: str}]:
    return list(map(lambda subject: { key: " ".join(str(value).split()) for (key, value) in subject.items() }, raw_schedule))


def beautify_classes(raw_schedule: [{str: [{str: str}]}], edited_subjects: [StudentSubject], settings: object, dates: [str] = []) -> [str]:
    schedule: [str] = []
    should_show_entire_semester: bool = (len(dates) == 0)
    
    if should_show_entire_semester:
        dates = WEEKDAYS
    else:
        dates.sort(key=lambda raw_date: date(date.today().year, int(raw_date[3:]), int(raw_date[:2])))
    
    if not should_show_entire_semester:
        dayoffs: {(int, int): str} = load_data(file=DAYOFFS)
    
    for raw_date in dates:
        if not should_show_entire_semester:
            (raw_day, raw_month) = raw_date.split(".")
            day_date: date = date(date.today().year, int(raw_month), int(raw_day))
            weekday: str = str(day_date.isoweekday())
            
            # Setting up date to search among dayoffs
            possible_dayoff = (day_date.day, day_date.month)
        else:
            weekday: str = str(raw_date)
        
        # Reseting the `subjects_list`. Adding the appropriate edited subjects to the schedule
        subjects_list: [(int, StudentSubject)] = [
            (subject.begin_hour, subject) for subject in edited_subjects if (
                subject.weekday == weekday and (subject.is_even is None or subject.is_even == is_asked_week_even)
            )
        ] if should_show_entire_semester or possible_dayoff not in dayoffs else []
        
        # Getting edited subjects begin hours
        edited_subjects_begin_hours: [int] = [ begin_hour for (begin_hour, _) in subjects_list ]
        
        if weekday in raw_schedule and (should_show_entire_semester or possible_dayoff not in dayoffs):
            raw_schedule[weekday] = refine_raw_schedule(raw_schedule[weekday])
            
            for subject in raw_schedule[weekday]:
                # No subjects - no schedule. For dayoffs
                if "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]: break
                
                # Clearing extra whitespaces from dates
                subject["dayDate"] = subject["dayDate"].replace(" ", "").replace(",", ", ")
                
                if not should_show_entire_semester:
                    # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
                    if (subject["dayDate"] == "неч") if is_week_even(day_date) else (subject["dayDate"] == "чет"): continue
                    
                    # Do not show subjects with certain dates (21.09) on other dates (28 сентября) if that's not asked
                    if "." in subject["dayDate"] and (
                        "{day}.{month}".format(day=int(raw_day), month=raw_month) not in subject["dayDate"] and
                        raw_date not in subject["dayDate"]
                    ): continue
                
                student_subject: StudentSubject = StudentSubject()
                
                student_subject.time = (subject["dayTime"], subject["disciplType"])
                
                # Do not show subject if there is its edited alternative
                if student_subject.begin_hour in edited_subjects_begin_hours: continue
                
                student_subject.building = subject["buildNum"]
                student_subject.auditorium = subject["audNum"]
                student_subject.dates = (subject["dayDate"], should_show_entire_semester)
                student_subject.title = subject["disciplName"]
                student_subject.type = (subject["disciplType"], subject.get("potok", "") != "")
                student_subject.lecturer = subject["prepodName"]
                student_subject.department = subject["orgUnitName"]
                
                subjects_list.append((student_subject.begin_hour, student_subject))
        
        # Sort by begin_hour
        subjects_list.sort(key=lambda subject: subject[0])
        
        daily_schedule: str = "".join([ (subject.get() if settings.is_schedule_size_full else subject.get_compact()) for (_, subject) in subjects_list ])
        
        if daily_schedule == "":
            daily_schedule = "\n\n{dayoff_message}".format(dayoff_message=dayoffs[possible_dayoff] if not should_show_entire_semester and possible_dayoff in dayoffs else "Выходной")
        
        schedule.append("".join([
            "*{weekday}*".format(weekday=WEEKDAYS[int(weekday)]) if should_show_entire_semester else "*{weekday}, {day} {month}*".format(
                weekday=WEEKDAYS.get(int(weekday), "Воскресенье"),
                day=int(raw_day), month=MONTHS[raw_month]
            ),
            daily_schedule
        ]))
    
    return schedule
    

def beautify_exams(raw_schedule: [{str: [{str: str}]}], settings: object) -> str:
    raw_schedule = refine_raw_schedule(raw_schedule)
    
    schedule: str = ""
    
    for subject in raw_schedule:
        time_place: str = "\n\n*[ {date}, {time} ][ {building}, {auditorium} ]*"
        
        if not settings.is_schedule_size_full:
            time_place = time_place.replace("][", "•").replace(" ]", "").replace("[ ", "")
        
        time_place = time_place.format(
            date=subject["examDate"], time=subject["examTime"],
            building=subject["buildNum"] + "ка", auditorium=subject["audNum"]
        )
        
        subject_name: str = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        lecturer: str = "\n@ {lecturer}".format(lecturer=subject["prepodName"].title()) if subject["prepodName"] else ""
        
        # Concatenate all the stuff above
        schedule = "".join([ schedule, time_place, subject_name, lecturer ])
    
    return schedule


def beautify_lecturers_classes(raw_schedule: {str: [{str: str}]}, settings: object, dates: [str] = []) -> [str]:
    schedule: [str] = []
    should_show_entire_semester: bool = (len(dates) == 0)
    
    if should_show_entire_semester:
        dates = WEEKDAYS
    else:
        dates.sort(key=lambda raw_date: date(date.today().year, int(raw_date[3:]), int(raw_date[:2])))
    
    initial_raw_schedule: {str: [{str: str}]} = raw_schedule
    
    for raw_date in dates:
        raw_schedule = dict(initial_raw_schedule)
        
        if not should_show_entire_semester:
            (raw_day, raw_month) = raw_date.split(".")
            day_date: date = date(date.today().year, int(raw_month), int(raw_day))
            weekday: str = str(day_date.isoweekday())
        else:
            weekday: str = str(raw_date)
        
        daily_schedule: str = ""
        
        previous_time: str = ""
        previous_date: str = ""
        
        if weekday not in raw_schedule:
            schedule.append("*{weekday}*\n\nНет занятий".format(
                weekday=WEEKDAYS[int(weekday)]
            ) if should_show_entire_semester else "*{weekday}, {day} {month}*\n\nНет занятий".format(
                weekday=WEEKDAYS.get(int(weekday), "Воскресенье"),
                day=int(raw_day), month=MONTHS[raw_month])
            )
            continue
        
        raw_schedule[weekday] = refine_raw_schedule(raw_schedule[weekday])
        
        # Clearing extra whitespaces from dates
        for (subject_index, subject) in enumerate(raw_schedule[weekday]):
            raw_schedule[weekday][subject_index]["dayDate"] = subject["dayDate"].replace(" ", "").replace(",", ", ")
        
        if not should_show_entire_semester:
            for subject in list(raw_schedule[weekday]):
                # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
                if (subject["dayDate"] == "неч") if is_week_even(day_date) else (subject["dayDate"] == "чет"):
                    raw_schedule[weekday].remove(subject)
                
                if "." in subject["dayDate"] and (
                    "{day}.{month}".format(day=int(raw_day), month=raw_month) not in subject["dayDate"] and
                    raw_date not in subject["dayDate"]
                ):
                    raw_schedule[weekday].remove(subject)
        
        # Setting subjects themselves
        for subject in raw_schedule[weekday]:
            if previous_time == subject["dayTime"] and previous_date == subject["dayDate"]: continue
            
            lecturer_subject: LecturerSubject = LecturerSubject()
            
            lecturer_subject.time = (subject["dayTime"], subject["disciplType"])
            lecturer_subject.building = subject["buildNum"]
            lecturer_subject.auditorium = subject["audNum"]
            lecturer_subject.dates = (subject["dayDate"], should_show_entire_semester)
            lecturer_subject.title = subject["disciplName"]
            lecturer_subject.type = (subject["disciplType"], False)
            
            previous_time = subject["dayTime"]
            previous_date = subject["dayDate"]
            
            for another_subject in raw_schedule[weekday]:
                if previous_time == another_subject["dayTime"] and previous_date == another_subject["dayDate"]:
                    lecturer_subject.groups.append(another_subject["group"])
            
            daily_schedule = "".join([
                daily_schedule,
                lecturer_subject.get() if settings.is_schedule_size_full else lecturer_subject.get_compact()
            ])
        
        if daily_schedule == "":
            daily_schedule = "\n\nНет занятий"
        
        schedule.append("".join([
            "*{weekday}*".format(
                weekday=WEEKDAYS[int(weekday)]
            ) if should_show_entire_semester else "*{weekday}, {day} {month}*".format(
                weekday=WEEKDAYS.get(int(weekday), "Воскресенье"),
                day=int(raw_day), month=MONTHS[raw_month]
            ),
            daily_schedule
        ]))
    
    return schedule

def beautify_lecturers_exams(raw_schedule: [{str: [{str: str}]}], settings: object) -> str:
    raw_schedule = refine_raw_schedule(raw_schedule)
    
    schedule: [(str, str)] = []
    
    for subject in raw_schedule:
        time_place: str = "\n\n*[ {date}, {time} ][ {building}, {auditorium} ]*"
        
        if not settings.is_schedule_size_full:
            time_place = time_place.replace("][", "•").replace(" ]", "").replace("[ ", "")
        
        time_place = time_place.format(
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
        
        if "(экз.)" in subject[1]: score_type: str = "".join([ "\n_", ScoreType.EXAM.value, "_\n" ])
        elif "(зач./оц.)" in subject[1]: score_type: str = "".join([ "\n_", ScoreType.COURSEWORK.value, "_\n" ])
        elif "(зач.)" in subject[1]: score_type: str = "".join([ "\n_", ScoreType.TEST.value, "_\n" ])
        else: score_type: str = "".join([ "\n_", ScoreType.OTHER.value, "_\n" ])
        
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
        
        scoretable.append((
            unstyled_title,
            "".join([ title, score_type, certification1, certification2, certification3, score_sum, debts ])
        ))
    
    return scoretable
