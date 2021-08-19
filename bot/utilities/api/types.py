from enum import Enum


class ResponseError(Enum):
    NO_RESPONSE = "kai.ru не отвечает🤷🏼‍♀️"
    NO_DATA = "Нет данных."
    NO_GROUP = (
        "Такой группы нет.\n"
        "Возможно, она появится позже, когда её внесут в каёвскую базу."
    )
    INCORRECT_CARD = "Неверный номер зачётки. Исправляйся."
    INCORRECT_SCHEDULE_TYPE = (
        "Ошибка передачи типа расписания.\n"
        "Напиши, пожалуйста, об этом разработчику."
    )


class ScheduleType(Enum):
    CLASSES = "schedule"
    EXAMS = "examSchedule"

class ClassType(Enum):
    LECTURE = "лек"
    PRACTICE = "пр"
    LAB = "л.р."
    CONSULTATION = "конс"
    MILITARY_TRAINING = "в.п."


class ScoreSubjectType(Enum):
    EXAM = "экзамен"
    COURSEWORK = "курсовая работа"
    TEST = "зачёт"
    OTHER = "другое"


class LocationType(Enum):
    BUILDING = "building"
    LIBRARY = "library"
    SPORTSCOMPLEX = "sportscomplex"
    DORM = "dorm"
