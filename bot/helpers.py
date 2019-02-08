from constants import SCHEDULE_URL
from constants import SCORE_URL
from constants import emoji
from constants import week

from datetime import datetime
from requests import get
from requests import post
from bs4      import BeautifulSoup

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
    with open("is_week_reversed", "w") as week_file:
        week_file.write("False") if is_week_reversed() else week_file.write("True")

# /classes & /exams
def get_schedule(type, kind, next=False):
    from student import student

    TODAYS_WEEKDAY = datetime.today().isoweekday()

    params = (
        ("p_p_id", "pubStudentSchedule_WAR_publicStudentSchedule10"),
        ("p_p_lifecycle", "2"),
        ("p_p_resource_id", "schedule" if type == "classes" else "examSchedule")
    )
    response = post(
        url=SCHEDULE_URL,
        params=params,
        data={ "groupId": student.get_group_number_for_schedule() }
    ).json()

    if not response:
        if kind == "today's":
            weekday = TODAYS_WEEKDAY
        elif kind == "tomorrow's":
            weekday = TODAYS_WEEKDAY + 1
        else:
            weekday = kind
    
        return "".join([
            "*{weekday}*\n\n".format(weekday=week[weekday]) if weekday else "",
            "Нет данных",
            "" if weekday else "."
        ])

    if type == "classes":
        if kind == "today's":
            schedule = beautify_classes(
                json_response=response[str(TODAYS_WEEKDAY)],
                weekday=TODAYS_WEEKDAY
            )
        elif kind == "tomorrow's":
            schedule = beautify_classes(
                json_response=response[str(TODAYS_WEEKDAY + 1)],
                weekday=TODAYS_WEEKDAY + 1
            )
        else:
            if str(kind) in response:
                schedule = beautify_classes(
                    json_response=response[str(kind)],
                    weekday=kind,
                    next=next
                )
            else:
                return "*{weekday}*\n\nВыходной".format(weekday=week[kind])
    else:
        schedule = beautify_exams(response)

    return schedule

def beautify_classes(json_response, weekday, next=False):
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
            if not is_even() and "чет" in subject["dayDate"] or is_even() and "неч" in subject["dayDate"]:
                continue
        else:
            if is_even() and "чет" in subject["dayDate"] or not is_even() and "неч" in subject["dayDate"]:
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
        schedule = "".join([schedule, time_place, date, subject_name, subject_type, teacher, department])
    
    return "".join([
        "*{weekday}*".format(weekday=week[weekday]),
        schedule if schedule and not is_day_off else "\n\nВыходной"
    ])

def beautify_exams(json_response):
    schedule = ""

    # Have no data to parse exams-json-response

    return schedule

# /score & associated stuff
def get_dict_of_list(type, params):
    page = get(url=SCORE_URL, params=params).content.decode("CP1251")
    soup = BeautifulSoup(page, "html.parser")

    selector = soup.find(name="select", attrs={ "name": type })

    keys = [option.text for option in selector.find_all("option")][1:]
    values = [option["value"] for option in selector.find_all("option")][1:]

    # Fixing bad quality response
    for i in range(1, len(keys)): keys[i - 1] = keys[i - 1][:keys[i - 1].find(keys[i])]

    return dict(zip(keys, values))
