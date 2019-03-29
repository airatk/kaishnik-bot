from datetime import datetime
from datetime import timedelta

class Subject:
    def __init__(self):
        self._time_place = "\n\n*[ {begin_time} - {end_time} ][ {building} ]{auditorium}*"
        self._dates      = "\n*[ {dates} ]*"
        self._title      = "\n*{title}*"
        self._type       = "\n_{type}_"

    def set_time_place(self, time, building, auditorium=""):
        hours, minutes = time.split(":")[0], time.split(":")[1]
        
        begin_time = datetime(1, 1, 1, int(hours), int(minutes))  # Year, month, day are filled with nonsence
        end_time = begin_time + timedelta(hours=1, minutes=30)  # Class time is 1.5h

        building = "СК Олимп" if building == "КАИ ОЛИМП" else "{building}ка".format(building=building)
        
        auditorium = "[ {auditorium} ]".format(auditorium=auditorium) if auditorium else ""
        
        self._time_place = self._time_place.format(
            begin_time=begin_time.strftime("%H:%M"),
            end_time=end_time.strftime("%H:%M"),
            building=building,
            auditorium=auditorium
        )

    def set_dates(self, dates):
        if "." in dates or "/" in dates or "(" in dates:
            self._dates = self._dates.format(dates=dates)
        else:
            self._dates = ""

    def set_title(self, title):
        self._title = self._title.format(title=title)

    def set_type(self, type):
        if type == "лек":
            self._type = "\n_лекция_"
        elif type == "пр":
            self._type = "\n_практика_"
        elif type == "л.р.":
            self._type = "\n_лабораторная работа_"
        else:
            self._type = ""

class StudentSubject(Subject):
    def __init__(self):
        super().__init__()
        
        self._teacher    = "\n@ {teacher}"
        self._department = "\n§  {department}"  # 2 whitespaces are not accident. It's UI

    def set_teacher(self, teacher):
        self._teacher = self._teacher.format(teacher=teacher.title()) if teacher else ""

    def set_department(self, department):
        self._department = self._department.format(department=department) if department else ""

    def get(self):
        return "".join([
            self._time_place,
            self._dates,
            self._title,
            self._type,
            self._teacher,
            self._department
        ])

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
            groups_output = "".join([groups_output, "\n• У группы {}".format(group)])
    
        return "".join([
            self._time_place,
            self._dates,
            self._title,
            self._type,
            groups_output
        ])
