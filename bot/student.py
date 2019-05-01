from bot.constants import SCHEDULE_URL
from bot.constants import SCORE_URL

from bot.helpers import beautify_classes
from bot.helpers import beautify_exams

from datetime import datetime
from datetime import timedelta

from requests import get
from requests import post

from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup

class Student:
    def __init__(
        self,
        institute=None,
        institute_id=None,
        year=None,
        name=None,
        student_card_number=None
    ):
        self._institute = institute
        self._institute_id = institute_id
        self._year = year
        self._group_number = None
        self._group_number_schedule = None
        self._another_group_number_schedule = None
        self._group_number_score = None
        self._name = name
        self._name_id = None
        self._names = {}
        self._student_card_number = student_card_number
    
        self._notes = []
        
        self._edited_subjects = []
        self._edited_class = None
    
        self._previous_message = None  # Gate System (GS)
    
    
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
    def another_group_number_schedule(self):
        return self._another_group_number_schedule
    
    @property
    def name(self):
        return self._name
    
    @property
    def names(self):
        return self._names
    
    @property
    def student_card_number(self):
        return self._student_card_number
    
    
    @property
    def notes(self):
        return self._notes
    
    
    @property
    def edited_subjects(self):
        return self._edited_subjects
    
    @property
    def edited_class(self):
        return self._edited_class
    
    
    @property
    def previous_message(self):
        return self._previous_message
    
    
    @institute.setter
    def institute(self, institute):
        self._institute = institute
    
    @year.setter
    def year(self, year):
        self._year = year
    
    @group_number.setter
    def group_number(self, group_number):
        # Setting raw group number
        self._group_number = group_number
        
        try:
            # Setting id of group number for schedule
            self._group_number_schedule = get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": "getGroupsURL",
                "query": group_number
            }).json()[0]["id"]
            
            # Setting id of group number for score
            if self._institute_id != "КИТ": self._group_number_score = self.get_dictionary_of(type="p_group")[group_number]
        except Exception:
            self._group_number = None
    
    @another_group_number_schedule.setter
    def another_group_number_schedule(self, group_number):
        if group_number is None:
            self._another_group_number_schedule = None
        else:
            try:
                self._another_group_number_schedule = get(url=SCHEDULE_URL, params={
                    "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                    "p_p_lifecycle": "2",
                    "p_p_resource_id": "getGroupsURL",
                    "query": group_number
                }).json()[0]["id"]
            except Exception:
                self._another_group_number_schedule = None
    
    @name.setter
    def name(self, name):
        # Setting raw name
        self._name = name
        
        try:
            # Setting id of name for score
            self._name_id = self.get_dictionary_of(type="p_stud")[name]
        except Exception:
            self._name = None
    
    @names.setter
    def names(self, given_names):
        self._names = given_names
    
    @student_card_number.setter
    def student_card_number(self, card):
        self._student_card_number = card


    @notes.setter
    def notes(self, given_notes):
        self._notes = given_notes
    
    
    @edited_subjects.setter
    def edited_subjects(self, given_edited_subjects):
        self._edited_subjects = given_edited_subjects
    
    @edited_class.setter
    def edited_class(self, given_edited_class):
        self._edited_class = given_edited_class


    @previous_message.setter
    def previous_message(self, message):
        self._previous_message = message
    
    
    # /edit
    def add_edited_class(self):
        self._edited_subjects.append(self._edited_class)
        
        self._edited_class = None
        self._previous_message = None  # Gate System (GS)
    
    # /classes & /exams
    def get_schedule(self, type, weekday=None, next=False):
        try:
            response = post(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": "schedule" if type == "classes" else "examSchedule"
            }, data={
                "groupId": self._group_number_schedule if self._another_group_number_schedule is None else self._another_group_number_schedule
            }).json()
        except ConnectionError:
            return "Сайт kai.ru не отвечает🤷🏼‍♀️"
        
        return beautify_classes(response, weekday, next, self._edited_subjects) if type == "classes" else beautify_exams(response)
    
    # /score & associated stuff
    def get_dictionary_of(self, type):
        try:
            page = get(url=SCORE_URL, params={
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_number_score
            }).content.decode("CP1251")
        except ConnectionError:
            return None
        
        soup = BeautifulSoup(page, "html.parser")
        selector = soup.find(name="select", attrs={ "name": type })
        
        keys = [ option.text for option in selector.find_all("option") ][1:]
        values = [ option["value"] for option in selector.find_all("option") ][1:]
        
        # Fixing bad quality response
        for i in range(1, len(keys)): keys[i - 1] = keys[i - 1].replace(keys[i], "")
        for i, key in enumerate(keys): keys[i] = key[:-1] if key.endswith(" ") else key
        
        return dict(zip(keys, values))
    
    def get_scoretable(self, semester):
        try:
            page = post(SCORE_URL, data={
                "p_sub": "",  # Unknown nonsense thing which is necessary
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_number_score,
                "p_stud": self._name_id,
                "p_zach": self._student_card_number,
                "semestr": semester
            }).content.decode("CP1251")
        except ConnectionError:
            return None

        soup = BeautifulSoup(page, features="html.parser")
        table = soup.html.find("table", { "id": "reyt" })
        
        if not table: return list()  # Returns empty list if student card number is incorrect
        
        subjects = []
        for row in table.find_all("tr"):
            subject = []
            for data in row.find_all("td"):
                subject.append(data.text if data.text else "-")
            subjects.append(subject)
        subjects = subjects[2:]

        return subjects
    
    # No setup - no conversation
    def is_not_set_up(self):
        return (
            self._institute is None or
            self._year is None or
            self._group_number is None or
            self._name is None or
            self._student_card_number is None
        )
