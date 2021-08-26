from enum import Enum


class ResponseError(Enum):
    NO_RESPONSE = "kai.ru не отвечает🤷🏼‍♀️"
    NO_DATA = "Нет данных."

    INCORRECT_BB_CREDENTIALS = "Неверный логин или пароль. Исправляйся."
    
    INCORRECT_SCHEDULE_TYPE = (
        "Ошибка передачи типа расписания.\n"
        "Напиши, пожалуйста, об этом разработчику."
    )
    INCORRECT_SCORE_DATA = (
        "Ошибка передачи параметров запроса баллов.\n"
        "Напиши, пожалуйста, об этом разработчику."
    )


class KaiRuDataType(Enum):
    SCORE = "attestacia"
    SCHEDULE = "raspisanie"

class ScheduleType(Enum):
    CLASSES = "schedule"
    EXAMS = "examSchedule"

class ClassType(Enum):
    LECTURE = "лек"
    PRACTICE = "пр"
    LAB = "л.р."
    CONSULTATION = "конс"
    MILITARY_TRAINING = "в.п."


class LocationType(Enum):
    BUILDING = "building"
    LIBRARY = "library"
    SPORTSCOMPLEX = "sportscomplex"
    DORM = "dorm"
