from datetime import datetime
from datetime import timedelta

from requests import post

from enum import Enum

from .constants import SCHEDULE_URL
from .constants import SCHEDULE_GROUP_ID
from .constants import WEEKDAYS
from .constants import MONTHS


class Schedule(Enum):
    CLASSES = 0
    EXAMS = 1


class StudentSubject:
    def __init__(self):
        self._time       = "\n\n{begin_time} - {end_time} ◦ "
        self._building   = "{building}, "
        self._auditorium = "{auditorium}"
        self._dates      = "\n[ {dates} ]"
        self._title      = "\n{title}"
        self._type       = " ({type})"
        self._teacher    = "\n@ {teacher}"
    
    
    @property
    def time(self):
        return self._time
    
    @property
    def building(self):
        return self._building
    
    @property
    def auditorium(self):
        return self._auditorium
    
    @property
    def dates(self):
        return self._dates
    
    @property
    def title(self):
        return self._title
    
    @property
    def type(self):
        return self._type
    
    @property
    def teacher(self):
        return self._teacher
    
    
    @time.setter
    def time(self, time):
        hours, minutes = int(time.split(":")[0]), int(time.split(":")[1])
        
        begin_time = datetime(1, 1, 1, hours, minutes)  # Year, month, day are filled with nonsence
        end_time = begin_time + timedelta(hours=1, minutes=30)  # Class duration is 1.5h
        
        self._time = self._time.format(
            begin_time=begin_time.strftime("%H:%M"),
            end_time=end_time.strftime("%H:%M")
        )
    
    @building.setter
    def building(self, building):
        self._building = self._building.format(
            building="СК Олимп" if building in [ "КАИ ОЛИМП", "СК Олимп" ] else "{}ка".format(building)
        )
    
    @auditorium.setter
    def auditorium(self, auditorium):
        self._auditorium = self._auditorium.format(auditorium=auditorium) if auditorium else ""
    
    @dates.setter
    def dates(self, dates):
        self._dates = self._dates.format(dates=dates) if "." in dates or "/" in dates or "(" in dates else ""

    @title.setter
    def title(self, title):
        self._title = self._title.format(title=title)
    
    @type.setter
    def type(self, type):
        if type == "лек":
            self._type = self._type.format(type="лекция")
        elif type == "пр":
            self._type = self._type.format(type="практика")
        elif type == "л.р.":
            self._type = self._type.format(type="лабораторная работа")
        else:
            self._type = ""

    @teacher.setter
    def teacher(self, teacher):
        self._teacher = self._teacher.format(teacher=teacher.title()) if teacher else ""
    
    
    def get(self):
        return "".join([
            self._time,
            self._building,
            self._auditorium,
            self._dates,
            self._title,
            self._type,
            self._teacher
        ])


def get_schedule(type, weekday=None, is_next=False):
    try:
        response = post(url=SCHEDULE_URL, params={
            "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "schedule" if type == Schedule.CLASSES else "examSchedule"
        }, data={
            "groupId": SCHEDULE_GROUP_ID
        }).json()
    except ConnectionError:
        return "Сайт kai.ru не отвечает🤷🏼‍♀️"
    
    return beautify_classes(response, weekday, is_next) if type == Schedule.CLASSES else beautify_exams(response)

def beautify_classes(json_response, weekday, is_next):
    date = datetime.today() + timedelta(days=(weekday - datetime.today().isoweekday()) + (7 if is_next else 0))
    
    if weekday == 7:
        return "Воскресенье, {day} {month}\n\nОднозначно выходной".format(
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )
    elif weekday == 8:
        weekday = 1
        is_next = True
    
    # No data - no schedule
    if not json_response:
        return "{weekday}, {day} {month}\n\nНет данных".format(
            weekday=WEEKDAYS[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )
    
    if str(weekday) in json_response:
        # Removing extraspaces
        json_response[str(weekday)] = [
            { key: " ".join(value.split()) for key, value in subject.items() } for subject in json_response[str(weekday)]
        ]
        
        schedule = ""
        
        for subject in json_response[str(weekday)]:
            # No subjects - no schedule. For day-offs
            if "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]: break
            
            # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
            if subject["dayDate"] == "неч" if (not is_even() if is_next else is_even()) else subject["dayDate"] == "чет": continue
            
            # Do not show subjects with certain dates (21.09) on other dates (28 сентября)
            day_month = "{}.{}".format(int(date.strftime("%d")), date.strftime("%m"))
            if "." in subject["dayDate"] and day_month not in subject["dayDate"]: continue

            studentSubject = StudentSubject()

            studentSubject.time = subject["dayTime"]
            studentSubject.building = subject["buildNum"]
            studentSubject.auditorium = subject["audNum"]
            studentSubject.dates = subject["dayDate"]
            studentSubject.title = subject["disciplName"]
            studentSubject.type = subject["disciplType"]
            studentSubject.teacher = subject["prepodName"]
            
            schedule = "".join([ schedule, studentSubject.get() ])

    return "".join([
        "{weekday}, {day} {month}".format(
            weekday=WEEKDAYS[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        ),
        schedule if schedule != "" else "\n\nВыходной"
    ])

def beautify_exams(json_response):
    # No data - no schedule
    if not json_response: return "Нет данных."
    
    # Removing extraspaces & standardizing values to string type
    json_response = [ {
            key: " ".join(str(value).split()) for key, value in subject.items()
        } for subject in json_response
    ]
    
    schedule = ""
    
    for subject in json_response:
        time_place = "\n\n{date}, {time} ◦ {building}, {auditorium}".format(
            date=subject["examDate"],
            time=subject["examTime"],
            building="{}ка".format(subject["buildNum"]),  # Make buildings look beautiful
            auditorium=subject["audNum"]
        )
        
        subject_name = "\n{subject_name}".format(subject_name=subject["disciplName"])
        
        teacher = "\n@ {teacher}".format(teacher=subject["prepodName"].title()) if subject["prepodName"] else ""
        
        # Concatenate all the stuff above
        schedule = "".join([ schedule, time_place, subject_name, teacher ])

    return schedule

def is_even():
    return datetime.today().isocalendar()[1] % 2 != 0
