from enum import Enum


class ScheduleType(Enum):
    CLASSES: str = "schedule"
    EXAMS: str = "examSchedule"

class ScoreDataType(Enum):
    YEARS: str = "p_kurs"
    GROUPS: str = "p_group"
    NAMES: str = "p_stud"


class ClassesOptionType(Enum):
    DAILY: str = "daily"
    WEEKDAYS: str = "weekdays"
    WEEKLY: str = "weekly"

class SubjectScoreType(Enum):
    EXAM: str = "экзамен"
    TEST: str = "зачёт"
    GRADED_TEST: str = "зачёт с оценкой"
    OTHER: str = "другое"


class ResponseError(Enum):
    NO_RESPONSE: str = "kai.ru не отвечает🤷🏼‍♀️"
    NO_DATA: str = "Нет данных."
    NO_GROUP: str = "Такой группы нет. Возможно, она появится позже, когда её внесут в каёвскую базу."
    INCORRECT_CARD: str = "Неверный номер зачётки. Исправляйся."
