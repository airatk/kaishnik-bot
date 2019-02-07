class Student:
    def __init__(self, group_number="4101", student_card_number="000000"):
        self.group_number = group_number
        self.student_card_number = student_card_number

    def get_group_number(self):
        return self.group_number

    def get_student_card_number(self):
        return self.student_card_number

    def set_group_number(self, group_number):
        self.group_number = group_number

    def set_student_card_number(self, student_card_number):
        self.student_card_number = student_card_number

student = Student()
