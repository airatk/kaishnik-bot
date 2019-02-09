from constants import SCHEDULE_URL
from helpers   import get_dict_of_list

from requests import get

class Student:
    def __init__(self,
                 institute=None,
                 year=None,
                 group_number_for_schedule=None,
                 group_number_for_score=None,
                 name=None,
                 student_card_number=None):
        self.institute = institute
        self.year = year
        self.group_number_for_schedule = group_number_for_schedule
        self.group_number_for_score = group_number_for_score
        self.name = name
        self.student_card_number = student_card_number

    def get_institute(self):
        return self.institute

    def get_year(self):
        return self.year

    def get_group_number_for_schedule(self):
        return self.group_number_for_schedule

    def get_group_number_for_score(self):
        return self.group_number_for_score

    def get_name(self):
        return self.name

    def get_student_card_number(self):
        return self.student_card_number

    def set_institute(self, institute):
        self.institute = institute

    def set_year(self, year):
        self.year = year

    def set_group_number_for_schedule(self, group_number):
        params = (
            ("p_p_id", "pubStudentSchedule_WAR_publicStudentSchedule10"),
            ("p_p_lifecycle", "2"),
            ("p_p_resource_id", "getGroupsURL"),
            ("query", group_number)
        )
    
        self.group_number_for_schedule = get(url=SCHEDULE_URL, params=params).json()[0]["id"]
    
    def set_group_number_for_score(self, group_number):
        params = (
            ("p_fac", student.get_institute()),
            ("p_kurs", student.get_year())
        )
                
        self.group_number_for_score = get_dict_of_list(type="p_group", params=params)[group_number]

    def set_name(self, name):
        params = (
            ("p_fac", student.get_institute()),
            ("p_kurs", student.get_year()),
            ("p_group", student.get_group_number_for_score())
        )
    
        self.name = get_dict_of_list(type="p_stud", params=params)[name]

    def set_student_card_number(self, student_card_number):
        self.student_card_number = student_card_number

student = Student()
