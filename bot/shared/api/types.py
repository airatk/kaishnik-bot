from enum import Enum


class ScheduleType(Enum):
    CLASSES = "schedule"
    EXAMS = "examSchedule"

class ScoreDataType(Enum):
    YEARS = "p_kurs"
    GROUPS = "p_group"
    NAMES = "p_stud"


class ClassesOptionType(Enum):
    DAILY = "daily"
    WEEKDAYS = "weekdays"
    WEEKLY = "weekly"

class SubjectScoreType(Enum):
    EXAM = "экзамен"
    TEST = "зачёт"
    GRADED_TEST = "зачёт с оценкой"
    OTHER = "другое"


class ResponseError(Enum):
    NO_RESPONSE = "kai.ru не отвечает🤷🏼‍♀️"
    NO_DATA = "Нет данных."
    NO_GROUP = "Такой группы нет. Возможно, она появится позже, когда её внесут в каёвскую базу."
    INCORRECT_CARD = "Неверный номер зачётки. Исправляйся."
