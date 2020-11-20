from enum import Enum


class ScheduleType(Enum):
    CLASSES: str = "schedule"
    EXAMS: str = "examSchedule"

class ScoreDataType(Enum):
    YEARS: str = "p_kurs"
    GROUPS: str = "p_group"
    NAMES: str = "p_stud"


class ClassesOptionType(Enum):
    SHOW: str = "classes-option-show"
    CHOOSE: str = "classes-option-choose"

class ScoreType(Enum):
    EXAM: str = "экзамен"
    COURSEWORK: str = "курсовая работа"
    TEST: str = "зачёт"
    OTHER: str = "другое"


class ResponseError(Enum):
    NO_RESPONSE: str = "kai.ru не отвечает🤷🏼‍♀️"
    NO_DATA: str = "Нет данных."
    NO_GROUP: str = (
        "Такой группы нет.\n"
        "Возможно, она появится позже, когда её внесут в каёвскую базу."
    )
    INCORRECT_CARD: str = "Неверный номер зачётки."
