from aiogram.types import Message

from bot.shared.api.helpers import beautify_classes
from bot.shared.api.helpers import beautify_exams
from bot.shared.api.helpers import beautify_scoretable
from bot.shared.api.constants import SCHEDULE_URL
from bot.shared.api.constants import SCORE_URL
from bot.shared.api.constants import P_SUB
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ScoreDataType
from bot.shared.api.subject import StudentSubject

from requests import get
from requests import post
from requests.exceptions import ConnectionError

from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup
from bs4.element import Tag

from enum import Enum


class Settings:
    class Option(Enum):
        IS_SCHEDULE_SIZE_FULL: str = "is-schedule-size-full"
        ARE_CLASSES_ON_DATES: str = "are-classes-on-dates"
    
    
    def __init__(self):
        self.is_schedule_size_full: bool = True
        self.are_classes_on_dates: bool = True
    
    
    def drop(self):
        self.__init__()


class Guard:
    def __init__(self):
        self.text: str = None
        self.message: Message = None
    
    
    def drop(self):
        self.__init__()


class Student:
    class Type(Enum):
        EXTENDED: str = "extended"
        COMPACT: str = "compact"
        
        GROUP_CHAT: str = "group-chat"
    
    
    def __init__(self):
        self.is_setup: bool = False
        self.type: Student.Type = None
        
        self.institute: str = None
        self.institute_id: str = None
        
        self.year: str = None
        
        self._group: str = None
        self.group_schedule_id: str = None
        self.group_score_id: str = None
        
        self.name: str = None
        self.name_id: str = None
        
        self.card: str = None
        
        self.notes: [str] = []
        self.edited_subjects: [StudentSubject] = []
        
        self.settings: Settings = Settings()
        
        
        # State savers
        self._another_group_schedule_id: str = None
        
        self.group_names: {str, str} = {}
        self.scoretable: [(str, str)] = None
        self.edited_subject: StudentSubject = None
        
        self.lecturers_names: [{str: str}] = None
        
        self.guard: Guard = Guard()
    
    
    @property
    def group(self) -> str:
        return self._group
    
    @property
    def another_group_schedule_id(self) -> str:
        return self._another_group_schedule_id
    
    
    @group.setter
    def group(self, new_value: str):
        self._group = new_value
        self.group_schedule_id = self._get_group_schedule_id()
    
    @another_group_schedule_id.setter
    def another_group(self, new_value: str):
        self._another_group_schedule_id = None if new_value is None else self._get_group_schedule_id(another_group=new_value)
    
    
    def _get_group_schedule_id(self, another_group: str = None) -> str:
        try:
            groups = get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": "getGroupsURL",
                "query": self._group if another_group is None else another_group
            }).json()
        except (ConnectionError, JSONDecodeError, IndexError, KeyError):
            return None
        
        if len(groups) != 1: return None  # User has to send exactly his group
        
        return groups[0]["id"]
    
    
    def get_schedule(self, TYPE: ScheduleType, weektype: str = None) -> [str]:
        is_own_group_asked: bool = self._another_group_schedule_id is None
        
        try:
            response: [{int: {str: str}}] = get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": TYPE.value,
                "groupId": self.group_schedule_id if is_own_group_asked else self._another_group_schedule_id
            }).json()
        except (ConnectionError, JSONDecodeError, IndexError, KeyError):
            return None
        
        if not response:
            return []
        
        self._another_group_schedule_id = None
        
        if TYPE is ScheduleType.CLASSES:
            return beautify_classes(response, weektype, self.edited_subjects if is_own_group_asked else [], self.settings)
        
        if TYPE is ScheduleType.EXAMS:
            return beautify_exams(response)
    
    
    def get_dictionary_of(self, TYPE: ScoreDataType) -> {str: str}:
        try:
            page: str = get(url=SCORE_URL, params={
                "p_fac": self.institute_id,
                "p_kurs": self.year,
                "p_group": self.group_score_id
            }).content.decode("CP1251")
            
            parsed_page: BeautifulSoup = BeautifulSoup(page, "html.parser")
            selector: Tag = parsed_page.find(name="select", attrs={ "name": TYPE.value })
            
            keys: [str] = [ option.text for option in selector.find_all("option") ][1:]
            values: [str] = [ option["value"] for option in selector.find_all("option") ][1:]
            
            # Fixing bad quality response
            for i in range(1, len(keys)): keys[i - 1] = keys[i - 1].replace(keys[i], "")
            for (i, key) in enumerate(keys): keys[i] = key[:-1] if key.endswith(" ") else key
        except (ConnectionError, AttributeError, KeyError, IndexError):
            return dict()
        else:
            return dict(zip(keys, values))
    
    def get_last_available_semester(self) -> int:
        try:
            page: str = post(SCORE_URL, data={
                "p_sub": P_SUB,
                "p_fac": self.institute_id,
                "p_kurs": self.year,
                "p_group": self.group_score_id,
                "p_stud": self.name_id,
                "p_zach": self.card
            }).content.decode("CP1251")
            
            parsed_page: BeautifulSoup = BeautifulSoup(page, "html.parser")
            selector: Tag = parsed_page.find(name="select", attrs={ "name": "semestr" })
            
            if not selector: return 0
            
            return max([ int(option["value"]) for option in selector.find_all("option") ])
        except ConnectionError:
            return None
    
    def get_scoretable(self, semester: str) -> [(str, str)]:
        try:
            page: str = post(SCORE_URL, data={
                "p_sub": P_SUB,
                "p_fac": self.institute_id,
                "p_kurs": self.year,
                "p_group": self.group_score_id,
                "p_stud": self.name_id,
                "p_zach": self.card,
                "semestr": semester
            }).content.decode("CP1251")
            
            parsed_page: BeautifulSoup = BeautifulSoup(page, features="html.parser")
            table: Tag = parsed_page.find(name="table", attrs={ "id": "reyt" })
            
            if not table: return []
            
            raw_scoretable: [[str]] = [ [ (data.text if data.text else "-") for data in row.find_all("td") ] for row in table.find_all("tr") ][2:]
            
            return beautify_scoretable(raw_scoretable)
        except ConnectionError:
            return None
