from bot.shared.api.helpers import beautify_classes
from bot.shared.api.helpers import beautify_exams
from bot.shared.api.helpers import beautify_scoretable
from bot.shared.api.constants import SCHEDULE_URL
from bot.shared.api.constants import SCORE_URL
from bot.shared.api.constants import P_SUB
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ScoreDataType
from bot.shared.api.types import ResponseError
from bot.shared.guard import Guard

from datetime import datetime
from datetime import timedelta

from requests import get
from requests import post

from bs4 import BeautifulSoup


class Student:
    def __init__(self):
        self._is_setup = False
        self._is_full = None
        
        self._institute = None
        self._institute_id = None
        
        self._year = None
        
        self._group = None
        self._group_schedule_id = None
        self._group_score_id = None
        
        self._another_group = None
        
        self._name = None
        self._name_id = None
        self._names = {}
        
        self._card = None
        
        self._scoretable = None
        
        self._notes = []
        
        self._edited_subjects = []
        self._edited_subject = None
        
        self._guard = Guard()
    
    
    @property
    def is_setup(self):
        return self._is_setup
    
    @property
    def is_full(self):
        return self._is_full
    
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
    def group(self):
        return self._group
    
    @property
    def group_schedule_id(self):
        return self._group_schedule_id
    
    @property
    def group_score_id(self):
        return self._group_score_id
    
    @property
    def another_group(self):
        return self._another_group
    
    @property
    def name(self):
        return self._name
    
    @property
    def name_id(self):
        return self._name_id
    
    @property
    def names(self):
        return self._names
    
    @property
    def card(self):
        return self._card
    
    @property
    def scoretable(self):
        return self._scoretable
    
    @property
    def notes(self):
        return self._notes
    
    @property
    def edited_subjects(self):
        return self._edited_subjects
    
    @property
    def edited_subject(self):
        return self._edited_subject
    
    @property
    def guard(self):
        return self._guard
    
    
    @is_setup.setter
    def is_setup(self, new_value):
        self._is_setup = new_value
    
    @is_full.setter
    def is_full(self, new_value):
        self._is_full = new_value
    
    @institute.setter
    def institute(self, new_value):
        self._institute = new_value

    @institute_id.setter
    def institute_id(self, new_value):
        self._institute_id = new_value
    
    @year.setter
    def year(self, new_value):
        self._year = new_value
    
    @group.setter
    def group(self, new_value):
        self._group = new_value
        self._group_schedule_id = self.get_schedule_id(group=new_value)
        self._group_score_id = self.get_dictionary_of(ScoreDataType.GROUPS).get(new_value) if self._is_full else None
    
    @another_group.setter
    def another_group(self, new_value):
        self._another_group = None if new_value is None else self.get_schedule_id(group=new_value)
    
    @name.setter
    def name(self, new_value):
        self._name = new_value
        self._name_id = self.get_dictionary_of(ScoreDataType.NAMES).get(new_value)
    
    @names.setter
    def names(self, new_value):
        self._names = new_value
    
    @card.setter
    def card(self, new_value):
        self._card = new_value
    
    @scoretable.setter
    def scoretable(self, new_value):
        self._scoretable = new_value
    
    @notes.setter
    def notes(self, new_value):
        self._notes = new_value
    
    @edited_subjects.setter
    def edited_subjects(self, new_value):
        self._edited_subjects = new_value
    
    @edited_subject.setter
    def edited_subject(self, new_value):
        self._edited_subject = new_value
    
    
    def get_schedule_id(self, group):
        try:
            return get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": "getGroupsURL",
                "query": group
            }).json()[0]["id"]
        except Exception:
            return None
    
    def get_schedule(self, TYPE, is_next=False):
        is_own_group_asked = self._another_group is None
        
        try:
            response = get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": TYPE.value,
                "groupId": self._group_schedule_id if is_own_group_asked else self._another_group
            }).json()
        except Exception:
            return None
        
        if not response: return []
        
        self._another_group = None

        if TYPE == ScheduleType.CLASSES:
            return beautify_classes(response, is_next, self._edited_subjects)
        elif TYPE == ScheduleType.EXAMS:
            return beautify_exams(response)
    
    
    def get_dictionary_of(self, TYPE) -> dict:
        try:
            page = get(url=SCORE_URL, params={
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_score_id
            }).content.decode("CP1251")
            
            soup = BeautifulSoup(page, "html.parser")
            selector = soup.find(name="select", attrs={ "name": TYPE.value })
            
            keys = [ option.text for option in selector.find_all("option") ][1:]
            values = [ option["value"] for option in selector.find_all("option") ][1:]
            
            # Fixing bad quality response
            for i in range(1, len(keys)): keys[i - 1] = keys[i - 1].replace(keys[i], "")
            for (i, key) in enumerate(keys): keys[i] = key[:-1] if key.endswith(" ") else key
        except Exception:
            return dict()
        else:
            return dict(zip(keys, values))
    
    def get_last_available_semester(self):
        try:
            page = post(SCORE_URL, data={
                "p_sub": P_SUB,
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_score_id,
                "p_stud": self._name_id,
                "p_zach": self._card
            }).content.decode("CP1251")
            
            soup = BeautifulSoup(page, "html.parser")
            selector = soup.find(name="select", attrs={ "name": "semestr" })
            
            if not selector: return 0
            
            return max([ int(option["value"]) for option in selector.find_all("option") ])
        except Exception:
            return None
    
    def get_scoretable(self, semester):
        try:
            page = post(SCORE_URL, data={
                "p_sub": P_SUB,
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_score_id,
                "p_stud": self._name_id,
                "p_zach": self._card,
                "semestr": semester
            }).content.decode("CP1251")
            
            soup = BeautifulSoup(page, features="html.parser")
            table = soup.html.find(name="table", attrs={ "id": "reyt" })
            
            if not table: return []
            
            raw_scoretable = [ [ (data.text if data.text else "-") for data in row.find_all("td") ] for row in table.find_all("tr") ][2:]
            
            return beautify_scoretable(raw_scoretable)
        except Exception:
            return None
