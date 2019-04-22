from bot.subject import StudentSubject
from bot.subject import LecturerSubject

from bot.constants import LECTURERS_SCHEDULE_URL
from bot.constants import WEEKDAYS
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
            weekday=WEEKDAYS[weekday],
            date=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )

    if str(weekday) not in json_response:
        return "*{weekday}, {day} {month}*\n\nВыходной".format(
            weekday=WEEKDAYS[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )

    # Removing extraspaces
    json_response[str(weekday)] = [
        { key: " ".join(value.split()) for key, value in subject.items() } for subject in json_response[str(weekday)]
    ]

    for subject in json_response[str(weekday)]:
        # No subjects - no schedule. For day-offs
        is_day_off = "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]
        if is_day_off:
            break
        
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if subject["dayDate"] == "неч" if is_even() else subject["dayDate"] == "чет":
                continue
        else:
            if subject["dayDate"] == "неч" if not is_even() else subject["dayDate"] == "чет":
                continue

        # Do not show subjects with certain dates (21.09) on other dates (28 сентября)
        day_month = "{}.{}".format(int(date.strftime("%d")), date.strftime("%m"))
        if "." in subject["dayDate"] and day_month not in subject["dayDate"]:
            continue

        studentSubject = StudentSubject()
        
        studentSubject.set_time(subject["dayTime"])
        studentSubject.set_building(subject["buildNum"])
        studentSubject.set_auditorium(subject["audNum"])
        studentSubject.set_dates(subject["dayDate"])
        studentSubject.set_title(subject["disciplName"])
        studentSubject.set_type(subject["disciplType"])
        studentSubject.set_teacher(subject["prepodName"])
        studentSubject.set_department(subject["orgUnitName"])

        schedule = "".join([schedule, studentSubject.get()])
    
    return "".join([
        "*{weekday}, {day} {month}*".format(
            weekday=WEEKDAYS[weekday],
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
    
    # Removing extraspaces & standardizing values to string type
    json_response = [
        { key: " ".join(str(value).split()) for key, value in subject.items() } for subject in json_response
    ]
    
    for subject in json_response:
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
    params = {
        "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
        "p_p_lifecycle": "2",
        "p_p_resource_id": "getLecturersURL",
        "query": name_part
    }

    return get(LECTURERS_SCHEDULE_URL, params=params).json()

def get_lecturers_schedule(prepod_login, type, weekday=None, next=False):
    params = {
        "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
        "p_p_lifecycle": "2",
        "p_p_resource_id": "schedule" if type == "l-classes" else "examSchedule"
    }
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
            weekday=WEEKDAYS[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )
    
    if str(weekday) not in json_response:
        return "*{weekday}, {day} {month}*\n\nНет занятий".format(
            weekday=WEEKDAYS[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        )
    
    # Removing extraspaces & standardizing values to string type
    json_response[str(weekday)] = [
        { key: " ".join(str(value).split()) for key, value in subject.items() } for subject in json_response[str(weekday)]
    ]
    
    # Getting rid of subjects which are not needed
    for subject in list(json_response[str(weekday)]):
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if subject["dayDate"] == "неч" if is_even() else subject["dayDate"] == "чет":
                json_response[str(weekday)].remove(subject)
        else:
            if subject["dayDate"] == "неч" if not is_even() else subject["dayDate"] == "чет":
                json_response[str(weekday)].remove(subject)
    
    # Finnaly, setting subjects themselves
    for subject in json_response[str(weekday)]:
        if previous_time == subject["dayTime"]:
            continue
        
        lecturerSubject = LecturerSubject()

        lecturerSubject.set_time(subject["dayTime"])
        lecturerSubject.set_building(subject["buildNum"])
        lecturerSubject.set_auditorium(subject["audNum"])
        lecturerSubject.set_dates(subject["dayDate"])
        lecturerSubject.set_title(subject["disciplName"])
        lecturerSubject.set_type(subject["disciplType"])
        
        previous_time = subject["dayTime"]
        
        for another_subject in json_response[str(weekday)]:
            if previous_time == another_subject["dayTime"]:
                lecturerSubject.groups.append(another_subject["group"])

        schedule = "".join([schedule, lecturerSubject.get()])

    return "".join([
        "*{weekday}, {day} {month}*".format(
            weekday=WEEKDAYS[weekday],
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
        ),
        schedule if schedule != "" else "\n\nНет занятий"
    ])

def beautify_lecturers_exams(json_response):
    schedule = ""
    
    if not json_response:
        return "Нет данных."

    # Removing extraspaces & standardizing values to string type
    json_response = [
        { key: " ".join(str(value).split()) for key, value in subject.items() } for subject in json_response
    ]

    for subject in json_response:
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
    
    certification1 = "\n• 1 аттестация: {gained} / {max}".format(gained=subject[2], max=subject[3])
    certification2 = "\n• 2 аттестация: {gained} / {max}".format(gained=subject[4], max=subject[5])
    certification3 = "\n• 3 аттестация: {gained} / {max}".format(gained=subject[6], max=subject[7])
    semesterSum = "\n◦ За семестр: {}".format(subject[8])
    
    debts = "\n\nДолги: {}".format(subject[10])
    
    return "".join([title, type, certification1, certification2, certification3, semesterSum, debts])


# /notes
def clarify_markdown(string):
    is_single = False
    
    for letter_index in range(len(string)):
        if string[letter_index] in "*_":
            index = letter_index
            is_single = not is_single
    
    return "".join([string[:index], "\\", string[index:]]) if is_single else string


# /metrics
class Metrics:
    def __init__(self):
        self._day = datetime.today().isoweekday()
        self._classes = 0
        self._score = 0
        self._lecturers = 0
        self._week = 0
        self._notes = 0
        self._exams = 0
        self._locations = 0
        self._card = 0
        self._brs = 0
        self._start = 0
        self._settings = 0
        self._unsetup = 0
        self._help = 0
        self._donate = 0
        self._unknown = 0
    
    @property
    def day(self):
        return self._day
    
    @property
    def classes(self):
        return self._classes
    
    @property
    def score(self):
        return self._score
    
    @property
    def lecturers(self):
        return self._lecturers
    
    @property
    def week(self):
        return self._week
    
    @property
    def notes(self):
        return self._notes
    
    @property
    def exams(self):
        return self._exams
    
    @property
    def locations(self):
        return self._locations
    
    @property
    def card(self):
        return self._card
    
    @property
    def brs(self):
        return self._brs
    
    @property
    def start(self):
        return self._start
    
    @property
    def settings(self):
        return self._settings
    
    @property
    def unsetup(self):
        return self._unsetup
    
    @property
    def help(self):
        return self._help
    
    @property
    def donate(self):
        return self._donate
    
    @property
    def unknown(self):
        return self._unknown
    
    @property
    def sum(self):
        return (
            self._classes +
            self._score +
            self._lecturers +
            self._week +
            self._notes +
            self._exams +
            self._locations +
            self._card +
            self._brs +
            self._start +
            self._settings +
            self._unsetup +
            self._donate +
            self._help +
            self._unknown
        )
    
    def zerofy(self):
        self._day = datetime.today().isoweekday()
        self._classes = 0
        self._score = 0
        self._lecturers = 0
        self._week = 0
        self._notes = 0
        self._exams = 0
        self._locations = 0
        self._card = 0
        self._brs = 0
        self._start = 0
        self._settings = 0
        self._unsetup = 0
        self._help = 0
        self._donate = 0
        self._unknown = 0
    
    def increment(self, command):
        if self._day != datetime.today().isoweekday():
            self.zerofy()
        
        if command == "classes":
            self._classes += 1
        elif command == "score":
            self._score += 1
        elif command == "lecturers":
            self._lecturers += 1
        elif command == "week":
            self._week += 1
        elif command == "notes":
            self._notes += 1
        elif command == "exams":
            self._exams += 1
        elif command == "locations":
            self._locations += 1
        elif command == "card":
            self._card += 1
        elif command == "brs":
            self._brs += 1
        elif command == "start":
            self._start += 1
        elif command == "settings":
            self._settings += 1
        elif command == "unsetup":
            self._unsetup += 1
        elif command == "help":
            self._help += 1
        elif command == "donate":
            self._donate += 1
        elif command == "unknown":
            self._unknown += 1
