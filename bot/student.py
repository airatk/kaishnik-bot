from constants import (
    SCHEDULE_URL, SCORE_URL,
    WEEK
)

from helpers import (
    beautify_classes, beautify_exams,
    load_users
)

from requests import get, post
from bs4      import BeautifulSoup

class Student:
    def __init__(
        self,
        institute=None,
        year=None,
        group_number_for_schedule=None,
        group_number_for_score=None,
        name=None,
        student_card_number=None,
        previous_message_text=None  # Used to let user enter lecturer's name. "/lecturers" command's text is saved in
    ):
        self.institute = institute
        self.year = year
        self.group_number_for_schedule = group_number_for_schedule
        self.group_number_for_score = group_number_for_score
        self.name = name
        self.student_card_number = student_card_number
        self.previous_message_text = previous_message_text

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
    
    def get_pmt(self):
        return self.previous_message_text

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
        self.group_number_for_score = self.get_dict_of_list(type="p_group")[group_number] if not group_number == "КИТ" else "КИТ"

    def set_name(self, name):
        self.name = self.get_dict_of_list(type="p_stud")[name] if not group_number == "КИТ" else "КИТ"

    def set_student_card_number(self, student_card_number):
        self.student_card_number = student_card_number

    def set_pmt(self, previous_message_text):
        self.previous_message_text = previous_message_text

    # /classes & /exams
    def get_schedule(self, type, weekday=None, next=False):
        params = (
            ("p_p_id", "pubStudentSchedule_WAR_publicStudentSchedule10"),
            ("p_p_lifecycle", "2"),
            ("p_p_resource_id", "schedule" if type == "classes" else "examSchedule")
        )
        
        response = post(
            url=SCHEDULE_URL,
            params=params,
            data={ "groupId": self.group_number_for_schedule }
        ).json()

        if not response:
            return "".join([
                "*{weekday}*\n\n".format(weekday=WEEK[weekday]) if weekday and weekday != 7 else "",
                "Нет данных", "" if weekday else "."
            ])

        if type == "classes":
            if weekday == 7:
                return "*Воскресенье*\n\nОднозначно выходной"
            elif weekday == 8:
                weekday = 1
                next = True
            
            if str(weekday) in response:
                schedule = beautify_classes(
                    json_response=response[str(weekday)],
                    weekday=weekday,
                    next=next
                )
            else:
                return "*{weekday}*\n\nВыходной".format(weekday=WEEK[weekday])
        else:
            schedule = beautify_exams(response)

        return schedule
    
    # /score & associated stuff
    def get_dict_of_list(self, type):
        params = (
            ("p_fac", self.institute),
            ("p_kurs", self.year),
            ("p_group", self.group_number_for_score)
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

    def get_score_table(self, semester):
        data = {
            "p_sub":   "",
            "p_fac":   self.institute,
            "p_kurs":  self.year,
            "p_group": self.group_number_for_score,
            "p_stud":  self.name,
            "p_zach":  self.student_card_number,
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
        return "Номер твоего студенческого билета и твоей зачётной книжки: *{card}*.".format(card=self.student_card_number)

    # No set up - no conversation
    def is_not_set_up(self):
        return self.institute is None or \
            self.year is None or \
            self.group_number_for_schedule is None or \
            self.group_number_for_score is None or \
            self.name is None

students = load_users()
