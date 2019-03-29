from bot.constants import SCHEDULE_URL
from bot.constants import SCORE_URL
from bot.constants import WEEK

from bot.helpers import beautify_classes
from bot.helpers import beautify_exams

from datetime import datetime
from datetime import timedelta

from requests import get
from requests import post

from bs4 import BeautifulSoup

class Student:
    def __init__(
        self,
        institute=None,
        institute_id=None,
        year=None,
        group_number=None,
        group_number_schedule=None,
        group_number_score=None,
        name=None,
        name_id=None,
        student_card_number=None,
        previous_message=None  # Used to recognize user's message sent after a command
    ):
        self._institute = institute
        self._institute_id = institute_id
        self._year = year
        self._group_number = group_number
        self._group_number_schedule = group_number_schedule
        self._group_number_score = group_number_score
        self._name = name
        self._name_id = name_id
        self._student_card_number = student_card_number
        self._previous_message = previous_message
    
    @property
    def institute(self):
        return self._institute
    
    @property
    def institute_id(self):
        return self._institute_id
    
    @property
    def year(self):
        return self._year
    
    @property
    def group_number(self):
        return self._group_number
    
    @property
    def group_number_schedule(self):
        return self._group_number_schedule
    
    @property
    def group_number_score(self):
        return self._group_number_score
    
    @property
    def name(self):
        return self._name
    
    @property
    def name_id(self):
        return self._name_id
    
    @property
    def student_card_number(self):
        return self._student_card_number
    
    @property
    def previous_message(self):
        return self._previous_message
    
    @institute.setter
    def institute(self, institute):
        self._institute = institute
    
    @institute_id.setter
    def institute_id(self, institute):
        self._institute_id = institute_id
    
    @year.setter
    def year(self, year):
        self._year = year
    
    @group_number.setter
    def group_number(self, group_number):
        self._group_number = group_number
    
    @group_number_schedule.setter
    def group_number_schedule(self, group_number):
        params = (
            ("p_p_id", "pubStudentSchedule_WAR_publicStudentSchedule10"),
            ("p_p_lifecycle", "2"),
            ("p_p_resource_id", "getGroupsURL"),
            ("query", group_number)
        )
    
        self._group_number_schedule = get(url=SCHEDULE_URL, params=params).json()[0]["id"]
    
    @group_number_score.setter
    def group_number_score(self, group_number):
        self._group_number_score = self.get_dictionary_of(type="p_group")[group_number]
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @name_id.setter
    def name_id(self, name):
        self._name_id = self.get_dictionary_of(type="p_stud")[name]
    
    @student_card_number.setter
    def student_card_number(self, card):
        self._student_card_number = card
    
    @previous_message.setter
    def previous_message(self, message):
        self._previous_message = message


    # /classes & /exams
    def get_schedule(self, type, weekday=None, next=False):
        params = (
            ("p_p_id", "pubStudentSchedule_WAR_publicStudentSchedule10"),
            ("p_p_lifecycle", "2"),
            ("p_p_resource_id", "schedule" if type == "classes" else "examSchedule")
        )
        data = {
            "groupId": self._group_number_schedule
        }
        
        response = post(url=SCHEDULE_URL, params=params, data=data).json()

        return beautify_classes(response, weekday, next) if type == "classes" else beautify_exams(response)
    
    # /score & associated stuff
    def get_dictionary_of(self, type):
        params = (
            ("p_fac", self._institute_id),
            ("p_kurs", self._year),
            ("p_group", self._group_number_score)
        )
    
        page = get(url=SCORE_URL, params=params).content.decode("CP1251")
        soup = BeautifulSoup(page, "html.parser")
        selector = soup.find(name="select", attrs={ "name": type })

        keys = [option.text for option in selector.find_all("option")][1:]
        values = [option["value"] for option in selector.find_all("option")][1:]

        # Fixing bad quality response
        for i in range(1, len(keys)): keys[i - 1] = keys[i - 1][:keys[i - 1].find(keys[i])]
        for i in range(len(keys)): keys[i] = keys[i][:-1] if keys[i][-1] == " " else keys[i]

        return dict(zip(keys, values))

    def get_scoretable(self, semester):
        data = {
            "p_sub":   "",  # Unknown nonsense thing which is necessary
            "p_fac":   self._institute_id,
            "p_kurs":  self._year,
            "p_group": self._group_number_score,
            "p_stud":  self._name_id,
            "p_zach":  self._student_card_number,
            "semestr": semester
        }
        
        page = post(SCORE_URL, data=data).content.decode("CP1251")
        soup = BeautifulSoup(page, features="html.parser")
        table = soup.html.find("table", { "id": "reyt" })

        # Returns None if student card number is incorrect or there is no data for certain semester
        if not table:
            return None

        subjects = []
        for row in table.find_all("tr"):
            subject = []
            for data in row.find_all("td"):
                subject.append(data.text if data.text else "-")
            subjects.append(subject)
        subjects = subjects[2:]

        return subjects

    # /card
    def get_card(self):
        return "Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(card=self._student_card_number)

    # No setup - no conversation
    def is_not_set_up(self):
        return (
            self._name is None or
            self._group_number is None or
            self._year is None or
            self._institute_id is None or
            self._student_card_number is None
        )
