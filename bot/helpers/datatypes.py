from enum import Enum


class ScheduleType(Enum):
    classes = "schedule"
    exams = "examSchedule"


class ScoreDataType(Enum):
    years = "p_kurs"
    groups = "p_group"
    names = "p_stud"
