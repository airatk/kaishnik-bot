from enum import Enum


class ResponseError(Enum):
    NO_RESPONSE: str = "kai.ru не отвечает🤷🏼‍♀️"
    NO_DATA: str = "Нет данных."
    NO_GROUP: str = (
        "Такой группы нет.\n"
        "Возможно, она появится позже, когда её внесут в каёвскую базу."
    )
    INCOMPLETE_GROUP_INPUT: str = "Номер группы нужно вводить полностью."
    INCORRECT_CARD: str = "Неверный номер зачётки. Исправляйся."
    INCORRECT_SCHEDULE_TYPE: str = (
        "Ошибка передачи типа расписания.\n"
        "Напиши, пожалуйста, об этом разработчику."
    )


class ExtendedLoginDataType(Enum):
    YEARS: str = "p_kurs"
    GROUPS: str = "p_group"
    NAMES: str = "p_stud"


class ScheduleType(Enum):
    CLASSES: str = "schedule"
    EXAMS: str = "examSchedule"

class ClassType(Enum):
    LECTURE: str = "лек"
    PRACTICE: str = "пр"
    LAB: str = "л.р."
    CONSULTATION: str = "конс"


class ScoreSubjectType(Enum):
    EXAM: str = "экзамен"
    COURSEWORK: str = "курсовая работа"
    TEST: str = "зачёт"
    OTHER: str = "другое"
