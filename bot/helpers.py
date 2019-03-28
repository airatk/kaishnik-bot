from bot.constants import LECTURERS_SCHEDULE_URL
from bot.constants import WEEK
from bot.constants import MONTHS

from datetime import datetime
from datetime import timedelta

from pickle import dump
from pickle import load
from pickle import HIGHEST_PROTOCOL

from requests import get
from requests import post


# Save data
def save_to(filename, object):
    with open(filename, "wb") as file:
        dump(object, file, HIGHEST_PROTOCOL)

def load_from(filename):
    with open(filename, "rb") as file:
        return load(file)


# /week
def get_week():
    return "Текущая неделя чётная." if is_even() else "Текущая неделя нечётная."

def is_even():
    return not is_week_reversed() if datetime.today().isocalendar()[1] % 2 == 0 else is_week_reversed()

def is_week_reversed():
    return load_from("data/is_week_reversed")


# /classes
def beautify_classes(json_response, weekday, next):
    schedule = ""
    is_day_off = False
    
    # Date of each day
    date = datetime.today() + timedelta(days=(weekday - datetime.today().isoweekday()) + (7 if next else 0))
    
    if weekday == 7:
        return "*Воскресенье, {day} {month}*\n\nОднозначно выходной".format(
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
            # This str(int(:string:)) was done to replace "01 апреля" by "1 апреля"
        )
    elif weekday == 8:
        weekday = 1
        next = True
    
    if not json_response:
        return "*{weekday}, {day} {month}*\n\nНет данных".format(
            weekday=WEEK[weekday],
            date=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )

    if str(weekday) not in json_response:
        return "*{weekday}, {day} {month}*\n\nВыходной".format(
            weekday=WEEK[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )

    for subject in json_response[str(weekday)]:
        # No subjects - no schedule. For day-offs
        is_day_off = "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]
        if is_day_off:
            break
    
        # Removing extraspaces
        subject = { property: " ".join(value.split()) for property, value in subject.items() }
    
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if subject["dayDate"] == "неч" if is_even() else subject["dayDate"] == "чет":
                continue
        else:
            if subject["dayDate"] == "неч" if not is_even() else subject["dayDate"] == "чет":
                continue

        # Do not show subjects with certain dates (21.09) on other dates (28 сентября)
        if "." in subject["dayDate"] and date.strftime("%d.%m") not in subject["dayDate"]:
            continue

        # Make buildings look beautiful
        building = "СК Олимп" if subject["buildNum"] == "КАИ ОЛИМП" else "".join([subject["buildNum"], "ка"])
        
        # Showing time in standart representation & adding the end time
        class_hours, class_minutes = subject["dayTime"].split(":")[0], subject["dayTime"].split(":")[1]
        begin_time = datetime(1, 1, 1, int(class_hours), int(class_minutes))  # Year, month, day are filled with nonsence
        end_time = begin_time + timedelta(hours=1, minutes=30)  # Class time is 1.5h
        
        time_place = "\n\n*[ {begin_time} - {end_time} ][ {building} ]{auditorium}*".format(
            begin_time=begin_time.strftime("%H:%M"),
            end_time=end_time.strftime("%H:%M"),
            building=building,
            auditorium=(" ".join(["[", subject["audNum"], "]"])) if subject["audNum"] else ""
        )
        
        # Show if a subject is supposed to be only on certain dates (like 21.09 or неч(6) or чет/неч)
        if "." in subject["dayDate"] or "/" in subject["dayDate"] or "(" in subject["dayDate"]:
            subject_dates = "\n*[ {subjects_dates} ]*".format(subjects_dates=subject["dayDate"])
        else:
            subject_dates = ""
        
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
        # 2 whitespaces (↑here) are not accident, it's UI
    
        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, subject_dates, subject_name, subject_type, teacher, department])
    
    return "".join([
        "*{weekday}, {day} {month}*".format(
            weekday=WEEK[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        ),
        schedule if schedule != "" and not is_day_off else "\n\nВыходной"
    ])

# /exams
def beautify_exams(json_response):
    schedule = ""
    
    if not json_response:
        return "Нет данных."
    
    for subject in json_response:
        # Removing extraspaces, standardizing values to string type
        subject = { property: " ".join(str(value).split()) for property, value in subject.items() }
        
        time_place = "\n\n*[ {date} ][ {time} ][ {building} ][ {auditorium} ]*".format(
            date=subject["examDate"],
            time=subject["examTime"],
            building="".join([subject["buildNum"], "ка"]),  # Make buildings look beautiful
            auditorium=subject["audNum"]
        )
        
        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        teacher = "\n@ {teacher}".format(teacher=subject["prepodName"].title()) if subject["prepodName"] else ""
        
        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, subject_name, teacher])

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

def get_lecturers_schedule(prepod_login, type, weekday=None, next=False):
    params = (
        ("p_p_id", "pubLecturerSchedule_WAR_publicLecturerSchedule10"),
        ("p_p_lifecycle", "2"),
        ("p_p_resource_id", "schedule" if type == "l-classes" else "examSchedule")
    )
    data = {
      "prepodLogin": prepod_login
    }

    response = post(url=LECTURERS_SCHEDULE_URL, params=params, data=data).json()

    return beautify_lecturers_classes(response, weekday, next) if type == "l-classes" else beautify_lecturers_exams(response)

def beautify_lecturers_classes(json_response, weekday, next):
    schedule = ""
    previous_time = ""
    
    # Date of each day
    date = datetime.today() + timedelta(days=(weekday - datetime.today().isoweekday()) + (7 if next else 0))
    
    if not json_response:
        return "*{weekday}, {day} {month}*\n\nНет данных".format(
            weekday=WEEK[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )
    
    if str(weekday) not in json_response:
        return "*{weekday}, {day} {month}*\n\nНет занятий".format(
            weekday=WEEK[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )
    
    for subject in json_response[str(weekday)]:
        # Removing extraspaces & standardizing values to string type
        subject = { property: " ".join(str(value).split()) for property, value in subject.items() }
    
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if subject["dayDate"] == "неч" if is_even() else subject["dayDate"] == "чет":
                continue
        else:
            if subject["dayDate"] == "неч" if not is_even() else subject["dayDate"] == "чет":
                continue

        # Gathering same time groups together
        if previous_time == subject["dayTime"]:
            schedule = "".join([schedule, "\n• У группы {}".format(subject["group"])])
            continue
        else:
            previous_time = subject["dayTime"]

        # Make buildings look beautiful
        building = "СК Олимп" if subject["buildNum"] == "КАИ ОЛИМП" else "".join([subject["buildNum"], "ка"])

        # Showing time in standart representation & adding the end time
        class_hours, class_minutes = subject["dayTime"].split(":")[0], subject["dayTime"].split(":")[1]
        begin_time = datetime(1, 1, 1, int(class_hours), int(class_minutes))  # Year, month, day are filled with nonsence
        end_time = begin_time + timedelta(hours=1, minutes=30)  # Class time is 1:30

        time_place = "\n\n*[ {begin_time} - {end_time} ][ {building} ]{auditorium}*".format(
            begin_time=begin_time.strftime("%H:%M"),
            end_time=end_time.strftime("%H:%M"),
            building=building,
            auditorium=("[ " + subject["audNum"] + " ]") if subject["audNum"] else ""
        )
        
        # Show if a subject is supposed to be only on certain date (like 21.09 or неч(6) or чет/неч)
        if "." in subject["dayDate"] or "/" in subject["dayDate"] or "(" in subject["dayDate"]:
            subject_dates = "\n*[ {subjects_dates} ]*".format(subjects_dates=subject["dayDate"])
        else:
            subject_dates = ""

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

        group = "\n• У группы {}".format(subject["group"])

        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, subject_dates, subject_name, subject_type, group])

    return "".join([
        "*{weekday}, {day} {month}*".format(
            weekday=WEEK[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        ),
        schedule if schedule != "" else "\n\nНет занятий"
    ])

def beautify_lecturers_exams(json_response):
    schedule = ""
    
    if not json_response:
        return "Нет данных."
    
    for subject in json_response:
        # Removing extraspaces, standardizing values to string type
        subject = { property: " ".join(str(value).split()) for property, value in subject.items() }
        
        time_place = "\n\n*[ {date} ][ {time} ][ {building} ][ {auditorium} ]*".format(
            date=subject["examDate"],
            time=subject["examTime"],
            building="".join([subject["buildNum"], "ка"]),  # Make buildings look beautiful
            auditorium=subject["audNum"]
        )
        
        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        group = "\n• У группы {group}".format(group=subject["group"])
        
        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, subject_name, group])
    
    return schedule


# /score
def get_subject_score(scoretable, subjects_num):
    subject = scoretable[subjects_num]
    
    title = "*{title}*".format(title=subject[1][:len(subject[1]) - 6])  # Erase (экз.) & (зач.)
    type = "\n_экзамен_\n" if "экз" in subject[1] else "\n_зачёт_\n"
    
    certification1 = "\n• 1 аттестация: {gained}/{max}".format(gained=subject[2], max=subject[3])
    certification2 = "\n• 2 аттестация: {gained}/{max}".format(gained=subject[4], max=subject[5])
    certification3 = "\n• 3 аттестация: {gained}/{max}".format(gained=subject[6], max=subject[7])
    semesterSum = "\n◦ За семестр: {}".format(subject[8])
    
    debts = "\n\nДолги: {}".format(subject[10])
    
    return "".join([title, type, certification1, certification2, certification3, semesterSum, debts])


# /metrics
class Metrics:
    def __init__(self):
        self.__day = datetime.today().isoweekday()
        self.__classes = 0
        self.__score = 0
        self.__lecturers = 0
        self.__week = 0
        self.__exams = 0
        self.__locations = 0
        self.__card = 0
        self.__brs = 0
        self.__start = 0
        self.__settings = 0
        self.__unsetup = 0
        self.__unknown = 0
    
    @property
    def day(self):
        return self.__day
    
    @property
    def classes(self):
        return self.__classes
    
    @property
    def score(self):
        return self.__score
    
    @property
    def lecturers(self):
        return self.__lecturers
    
    @property
    def week(self):
        return self.__week
    
    @property
    def exams(self):
        return self.__exams
    
    @property
    def locations(self):
        return self.__locations
    
    @property
    def card(self):
        return self.__card
    
    @property
    def brs(self):
        return self.__brs
    
    @property
    def start(self):
        return self.__start
    
    @property
    def settings(self):
        return self.__settings
    
    @property
    def unsetup(self):
        return self.__unsetup
    
    @property
    def unknown(self):
        return self.__unknown
    
    def increment(self, command):
        if self.__day != datetime.today().isoweekday():
            self.zerofy()
        
        if command == "classes":
            self.__classes += 1
        elif command == "score":
            self.__score += 1
        elif command == "lecturers":
            self.__lecturers += 1
        elif command == "week":
            self.__week += 1
        elif command == "exams":
            self.__exams += 1
        elif command == "locations":
            self.__locations += 1
        elif command == "card":
            self.__card += 1
        elif command == "brs":
            self.__brs += 1
        elif command == "start":
            self.__start += 1
        elif command == "settings":
            self.__settings += 1
        elif command == "unsetup":
            self.__unsetup += 1
        elif command == "unknown":
            self.__unknown += 1
    
    def sum(self):
        return (
            self.__classes +
            self.__score +
            self.__lecturers +
            self.__week +
            self.__exams +
            self.__locations +
            self.__card +
            self.__brs +
            self.__start +
            self.__settings +
            self.__unsetup +
            self.__unknown
        )
    
    def zerofy(self):
        self.__day = datetime.today().isoweekday()
        self.__classes = 0
        self.__score = 0
        self.__lecturers = 0
        self.__week = 0
        self.__exams = 0
        self.__locations = 0
        self.__card = 0
        self.__brs = 0
        self.__start = 0
        self.__settings = 0
        self.__unsetup = 0
        self.__unknown = 0
