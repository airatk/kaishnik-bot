from constants import emoji
from constants import week

from datetime import datetime
from requests import get
from requests import post

# Set MSK timezone
import os, time; os.environ["TZ"] = "MSK"; time.tzset()

# /week
def get_week():
    return "Текущая неделя чётная." if is_even() else "Текущая неделя нечётная."

def is_even():
    if datetime.today().isocalendar()[1] % 2 == 0:
        return True if not is_week_reversed() else False
    else:
        return False if not is_week_reversed() else True

def is_week_reversed():
    with open("is_week_reversed", "r") as week_file:
        return True if week_file.read() == "True" else False

def reverse_week_in_file():
    is_true = is_week_reversed()

    with open("is_week_reversed", "w") as week_file:
        week_file.write("False") if is_true else week_file.write("True")

# /classes & /exams
def get_schedule(type, kind, group_number, next=False):
    def get_group_id(group_number):
        params = (
            ('p_p_id', 'pubStudentSchedule_WAR_publicStudentSchedule10'),
            ('p_p_lifecycle', '2'),
            ('p_p_resource_id', 'getGroupsURL'),
            ('query', group_number)
        )
        return get('https://kai.ru/raspisanie', params=params).json()[0]["id"]
    
    params = (
        ('p_p_id', 'pubStudentSchedule_WAR_publicStudentSchedule10'),
        ('p_p_lifecycle', '2'),
        ('p_p_resource_id', "schedule" if type == "classes" else "examSchedule"),
    )
    data = {
        'groupId': get_group_id(group_number),
    }
    response = post('https://kai.ru/raspisanie', params=params, data=data).json()

    if type == "classes":
        if kind == "today's":
            todays_weekday = datetime.today().isoweekday()
            schedule = beautify_classes(
                json_response=response["{todays_weekday}".format(todays_weekday=todays_weekday)],
                weekday=todays_weekday
            )
        elif kind == "tomorrow's":
            tomorrows_weekday = datetime.today().isoweekday() + 1
            schedule = beautify_classes(
                json_response=response["{tomorrows_weekday}".format(tomorrows_weekday=tomorrows_weekday)],
                weekday=tomorrows_weekday
            )
        else:
            schedule = beautify_classes(
                json_response=response["{weekday}".format(weekday=kind)],
                weekday=kind,
                next=next
            )
    else:
        schedule = beautify_exams(response)

    return schedule

def beautify_classes(json_response, weekday, next=False):
    schedule = ""
    
    for subject in json_response:
        # Removing extraspaces
        for property in subject:
            subject[property] = " ".join(subject[property].split())
    
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if not is_even() and "чет" == subject["dayDate"] or is_even() and "неч" == subject["dayDate"]:
                continue
        else:
            if is_even() and "чет" == subject["dayDate"] or not is_even() and "неч" == subject["dayDate"]:
                continue
    
        # Make buildings look beautiful
        if subject["buildNum"] == "КАИ ОЛИМП":
            building = "СК Олимп"
        elif subject["buildNum"] == "1":
            building = "1ый дом"
        else:
            building = ''.join([subject["buildNum"], "ка"])
    
        time_place = "\n\n*[ {time} ][ {building} ][ {auditorium} ]*".format(
            time=subject["dayTime"],
            building=building,
            auditorium=subject["audNum"] if subject["audNum"] else "-"
        )
        
        # Show if a subject is supposed to be only on certain date (like 21.09 or 07.11)
        date = "\n*[ Только {date} ]*".format(date=subject["dayDate"]) if "." in subject["dayDate"] else ""
        
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
        schedule = ''.join([schedule, time_place, date, subject_name, subject_type, teacher, department])

    return ''.join([
        "*{weekday}*".format(weekday=week[weekday]),
        schedule if schedule and not "День консультаций" in subject["disciplName"] else "\n\nВыходной"
    ])

def beautify_exams(json_response):
    schedule = ""

    # Have no data to parse exams json response

    return schedule
