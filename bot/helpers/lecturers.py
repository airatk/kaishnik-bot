from bot.helpers           import is_even
from bot.helpers.subject   import LecturerSubject
from bot.helpers.datatypes import ScheduleType
from bot.helpers.constants import LECTURERS_SCHEDULE_URL
from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import MONTHS

from datetime import datetime
from datetime import timedelta

from requests            import get
from requests.exceptions import ConnectionError


def get_lecturers_names(name_part):
    try:
        return get(LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getLecturersURL",
            "query": name_part
        }).json()
    except ConnectionError:
        return None

def get_lecturers_schedule(lecturer_id, type, weekday=None, next=False):
    try:
        response = get(url=LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": type.value,
            "prepodLogin": lecturer_id
        }).json()
    except ConnectionError:
        return [ "Сайт kai.ru не отвечает🤷🏼‍♀️" ]
    
    if not response: return [ "Нет данных." ]
    
    return beautify_lecturers_classes(response, next) if type == ScheduleType.classes else beautify_lecturers_exams(response)


def beautify_lecturers_classes(json_response, next):
    weekly_schedule = []
    
    today = datetime.today() + timedelta(days=7 if next else 0)
    todays_weekday = today.isoweekday()
    
    for weekday in WEEKDAYS:
        date = today + timedelta(days=weekday - todays_weekday)  # Date of each day
        
        daily_schedule = ""
        previous_time = ""
        
        if str(weekday) not in json_response:
            weekly_schedule.append("*{weekday}, {day} {month}*\n\nНет занятий".format(
                weekday=WEEKDAYS[weekday],
                day=int(date.strftime("%d")),
                month=MONTHS[date.strftime("%m")]
            ))
            continue
        
        # Removing extraspaces & standardizing values to string type
        json_response[str(weekday)] = [ {
                key: " ".join(str(value).split()) for key, value in subject.items()
            } for subject in json_response[str(weekday)]
        ]
        
        # Getting rid of subjects which are not needed
        for subject in list(json_response[str(weekday)]):
            # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
            if subject["dayDate"] == "неч" if (not is_even() if next else is_even()) else subject["dayDate"] == "чет":
                json_response[str(weekday)].remove(subject)
        
        # Finnaly, setting subjects themselves
        for subject in json_response[str(weekday)]:
            if previous_time == subject["dayTime"]: continue
            
            lecturerSubject = LecturerSubject()

            lecturerSubject.time = subject["dayTime"]
            lecturerSubject.building = subject["buildNum"]
            lecturerSubject.auditorium = subject["audNum"]
            lecturerSubject.dates = subject["dayDate"]
            lecturerSubject.title = subject["disciplName"]
            lecturerSubject.type = subject["disciplType"]
            
            previous_time = subject["dayTime"]
            
            for another_subject in json_response[str(weekday)]:
                if previous_time == another_subject["dayTime"]:
                    lecturerSubject.groups.append(another_subject["group"])

            daily_schedule = "".join([ daily_schedule, lecturerSubject.get() ])
        
        weekly_schedule.append("".join([
            "*{weekday}, {day} {month}*".format(
                weekday=WEEKDAYS[weekday],
                day=int(date.strftime("%d")),
                month=MONTHS[date.strftime("%m")]
            ),
            daily_schedule if daily_schedule != "" else "\n\nНет занятий"
        ]))

    return weekly_schedule

def beautify_lecturers_exams(json_response):
    # Removing extraspaces & standardizing values to string type
    json_response = [ {
            key: " ".join(str(value).split()) for key, value in subject.items()
        } for subject in json_response
    ]
    
    schedule = []
    
    for subject in json_response:
        time_place = "\n\n*[ {date}, {time} ][ {building}, {auditorium} ]*".format(
            date=subject["examDate"],
            time=subject["examTime"],
            building="{}ка".format(subject["buildNum"]),  # Make buildings look beautiful
            auditorium=subject["audNum"]
        )
        
        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        group = "\n• У группы {group}".format(group=subject["group"])
        
        # To sort by date
        functional_date_entities = subject["examDate"].split(".")
        functional_date = "".join([ functional_date_entities[1], functional_date_entities[0] ])
        
        schedule.append((functional_date, "".join([ time_place, subject_name, group ])))
    
    schedule.sort(key=lambda subject: subject[0])
    
    return [ "".join([ subject for _, subject in schedule ]) ]
