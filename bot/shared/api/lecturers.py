from bot.shared.api.helpers import beautify_lecturers_classes
from bot.shared.api.helpers import beautify_lecturers_exams
from bot.shared.api.constants import LECTURERS_SCHEDULE_URL
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError

from requests import get


def get_lecturers_names(name_part) -> list:
    try:
        return get(LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getLecturersURL",
            "query": name_part
        }).json()
    except Exception:
        return None

def get_lecturers_schedule(lecturer_id, TYPE, weekday=None, is_next=False):
    try:
        response = get(url=LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": TYPE.value,
            "prepodLogin": lecturer_id
        }).json()
    except Exception:
        return None
    
    if not response: return []

    if TYPE == ScheduleType.CLASSES:
        return beautify_lecturers_classes(response, is_next)
    elif TYPE == ScheduleType.EXAMS:
        return beautify_lecturers_exams(response)
