from constants import (
    WEEK,
    LECTURERS_SCHEDULE_URL
)

from datetime import datetime
from pickle   import dump, load, HIGHEST_PROTOCOL
from requests import get, post

# No user data is lost anymore!
def save_users(users):
    with open("users.pkl", "wb") as users_file:
        dump(users, users_file, HIGHEST_PROTOCOL)

def load_users():
    with open("users.pkl", "rb") as users_file:
        return load(users_file)

# /week
def get_week():
    return "Текущая неделя чётная." if is_even() else "Текущая неделя нечётная."

def is_even():
    return not is_week_reversed() if datetime.today().isocalendar()[1] % 2 == 0 else is_week_reversed()

def is_week_reversed():
    with open("is_week_reversed", "r") as week_file:
        return "True" in week_file.read()

def reverse_week_in_file():
    with open("is_week_reversed", "r+") as week_file:
        week_file.write("False") if is_week_reversed() else week_file.write("True")

# /classes
def beautify_classes(json_response, weekday, next):
    schedule = ""
    is_day_off = False
    
    for subject in json_response:
        # No subjects - no schedule. For day-offs
        is_day_off = "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]
        if is_day_off:
            break
    
        # Removing extraspaces
        for property in subject:
            subject[property] = " ".join(subject[property].split())
    
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if not is_even() and subject["dayDate"] == "чет" or is_even() and subject["dayDate"] == "неч":
                continue
        else:
            if is_even() and subject["dayDate"] == "чет" or not is_even() and subject["dayDate"] == "неч":
                continue
    
        # Make buildings look beautiful
        if subject["buildNum"] == "КАИ ОЛИМП":
            building = "СК Олимп"
        elif subject["buildNum"] == "1":
            building = "1ый дом"
        else:
            building = "".join([subject["buildNum"], "ка"])
    
        time_place = "\n\n*[ {time} ][ {building} ][ {auditorium} ]*".format(
            time=subject["dayTime"],
            building=building,
            auditorium=subject["audNum"] if subject["audNum"] else "-"
        )
        
        # Show if a subject is supposed to be only on certain date (like 21.09 or 07.11 or неч(6) or чет/неч неч/чет)
        if "." in subject["dayDate"] or "/" in subject["dayDate"] or "(" in subject["dayDate"]:
            date = "\n*[ !!! {date} ]*".format(date=subject["dayDate"])
        else:
            date = ""
        
        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        # Make subject types look beautiful
        if subject["disciplType"] == "лек":
            subject_type = "\n_лекция_"
        elif subject["disciplType"] == "пр":
            subject_type = "\n_практика_"
        elif subject["disciplType"] == "л.р.":
            subject_type = "\n_лабораторная работа_"
        else:
            subject_type = ""

        # Do not show empty strings
        teacher = "\n@ {teacher}".format(teacher=subject["prepodName"].title()) if subject["prepodName"] else ""
        department = "\n§  {department}".format(department=subject["orgUnitName"]) if subject["orgUnitName"] else ""
    
        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, date, subject_name, subject_type, teacher, department])
    
    return "".join([
        "*{weekday}*".format(weekday=WEEK[weekday]),
        schedule if schedule and not is_day_off else "\n\nВыходной"
    ])

# /exams
def beautify_exams(json_response):
    schedule = ""

    # Have no data to parse exams-json-response

    return schedule

# /lecturers
def get_lecturers_names(name_part):
    params = (
        ("p_p_id", "pubLecturerSchedule_WAR_publicLecturerSchedule10"),
        ("p_p_lifecycle", "2"),
        ("p_p_resource_id", "getLecturersURL"),
        ("query", name_part)
    )

    return get(LECTURERS_SCHEDULE_URL, params=params).json()

def get_lecturers_schedule(prepod_login, type, weekday=None):
    params = (
        ("p_p_id", "pubLecturerSchedule_WAR_publicLecturerSchedule10"),
        ("p_p_lifecycle", "2"),
        ("p_p_resource_id", "schedule" if type == "l_c" else "examSchedule")
    )
    data = {
      "prepodLogin": prepod_login
    }

    schedule = post(LECTURERS_SCHEDULE_URL, params=params, data=data).json()

    if not schedule:
        return "*{weekday}*\n\nНет данных".format(weekday=WEEK[weekday]) if weekday else "Нет данных."

    if type == "l_c":
        return beautify_lecturers_classes(schedule, weekday)
    else:
        return beautify_lecturers_exams(schedule)

def beautify_lecturers_classes(json_response, weekday):
    schedule = ""

    if str(weekday) not in json_response:
        return "*{weekday}*\n\nНет занятий".format(weekday=WEEK[weekday])

    for subject in json_response[str(weekday)]:
        # Removing extraspaces, standardizing values to string type
        for property in subject:
            subject[property] = str(subject[property])
            subject[property] = " ".join(subject[property].split())
    
        # Make buildings look beautiful
        if subject["buildNum"] == "КАИ ОЛИМП":
            building = "СК Олимп"
        elif subject["buildNum"] == "1":
            building = "1ый дом"
        else:
            building = "".join([subject["buildNum"], "ка"])
    
        time_place = "\n\n*[ {time} ][ {building} ][ {auditorium} ]*".format(
            time=subject["dayTime"],
            building=building,
            auditorium=subject["audNum"] if subject["audNum"] else "-"
        )
        
        if subject["dayDate"] and "неч/чет" not in subject["dayDate"] and "чет/неч" not in subject["dayDate"]:
            date = "\n*[ {date} ]*".format(date=subject["dayDate"])
        else:
            date = ""

        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        # Make subject types look beautiful
        if subject["disciplType"] == "лек":
            subject_type = "\n_лекция_"
        elif subject["disciplType"] == "пр":
            subject_type = "\n_практика_"
        elif subject["disciplType"] == "л.р.":
            subject_type = "\n_лабораторная работа_"
        else:
            subject_type = ""

        group = "\n# У группы {group}".format(group=subject["group"])

        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, date, subject_name, subject_type, group])

    return "".join(["*{weekday}*".format(weekday=WEEK[weekday]), schedule])

def beautify_lecturers_exams(json_response):
    schedule = ""

    for subject in json_response:
        # Removing extraspaces, standardizing values to string type
        for property in subject:
            subject[property] = str(subject[property])
            subject[property] = " ".join(subject[property].split())
            
        time_place = "\n\n*[ {date} ][ {time} ][ {building} ][ {auditorium} ]*".format(
            date=subject["examDate"],
            time=subject["examTime"],
            # Make buildings look beautiful
            building="1ый дом" if subject["buildNum"] == "1" else "".join([subject["buildNum"], "ка"]),
            auditorium=subject["audNum"] if subject["audNum"] else "-"
        )

        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])

        group = "\n# У группы {group}".format(group=subject["group"])

        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, subject_name, group])

    return schedule

# /score
def get_subject_score(score_table, subjects_num):
    subject = score_table[subjects_num]

    title = "*{title}*".format(title=subject[1][:len(subject[1]) - 6])
    type = "\n_экзамен_\n" if "экз" in subject[1] else "\n_зачёт_\n"

    certification1 = "\n• 1 аттестация: {gained}/{max}".format(gained=subject[2], max=subject[3])
    certification2 = "\n• 2 аттестация: {gained}/{max}".format(gained=subject[4], max=subject[5])
    certification3 = "\n• 3 аттестация: {gained}/{max}".format(gained=subject[6], max=subject[7])
    preresult      = "\n- За семестр: {preresult}/50".format(preresult=subject[8]) # Which is sum of the above

    debts = "\n\nДолги: {gained}".format(gained=subject[10])

    return "".join([title, type, certification1, certification2, certification3, preresult, debts])
