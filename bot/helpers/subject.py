from abc import ABC
from abc import abstractmethod

from datetime import datetime
from datetime import timedelta


class Subject(ABC):
    def __init__(self):
        self._time       = "\n\n*[ {begin_time} - {end_time} ]"
        self._building   = "[ {building}"
        self._auditorium = "{auditorium} ]"
        self._dates      = "\n[ {dates} ]"
        self._title      = "\n{title}*"
        self._type       = "\n_{type}_"
        
        self._begin_time = None
    
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
    
    @time.setter
    def time(self, time):
        self._begin_time = time
        
        hours, minutes = int(time.split(":")[0]), int(time.split(":")[1])
        
        self._begin_hour = hours
        
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
        self._auditorium = self._auditorium.format(auditorium=(", " + auditorium) if auditorium else "")
    
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

    @abstractmethod
    def get(self):
        pass


class StudentSubject(Subject):
    def __init__(self):
        super().__init__()
        
        self._teacher    = "\n@ {teacher}"
        self._department = "\n§ {department}"
        
        self._is_even = None
        self._weekday = None
        self._begin_hour = None
    
    @property
    def teacher(self):
        return self._teacher
    
    @property
    def department(self):
        return self._department
    
    @teacher.setter
    def teacher(self, teacher):
        self._teacher = self._teacher.format(teacher=teacher.title()) if teacher else ""
    
    @department.setter
    def department(self, department):
        self._department = self._department.format(department=department) if department else ""
    
    
    @property
    def is_even(self):
        return self._is_even
    
    @property
    def weekday(self):
        return self._weekday
    
    @property
    def begin_hour(self):
        return self._begin_hour
    
    @is_even.setter
    def is_even(self, given_is_even):
        self._is_even = given_is_even
    
    @weekday.setter
    def weekday(self, given_weekday):
        self._weekday = given_weekday
    
    @begin_hour.setter
    def begin_hour(self, given_begin_hour):
        self._begin_hour = given_begin_hour
    
    
    def get(self):
        return "".join([
            self._time,
            self._building,
            self._auditorium,
            self._dates,
            self._title,
            self._type,
            self._teacher,
            self._department
        ])

    def get_simple(self):
        return " ".join([ self._begin_time, self._title ]).replace("\n", "").replace("*", "")


class LecturerSubject(Subject):
    def __init__(self):
        super().__init__()
        
        self._groups = []
    
    @property
    def groups(self):
        return self._groups
    
    def get(self):
        groups_output = ""
        
        for group in self._groups:
            groups_output = "".join([ groups_output, "\n• У группы {}".format(group) ])
        
        return "".join([
            self._time,
            self._building,
            self._auditorium,
            self._dates,
            self._title,
            self._type,
            groups_output
        ])
