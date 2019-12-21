from bot.shared.api.helpers import beautify_lecturers_classes
from bot.shared.api.helpers import beautify_lecturers_exams
from bot.shared.api.constants import LECTURERS_SCHEDULE_URL
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError

from requests import get


def get_lecturers_names(name_part: str) -> [{str, str}]:
    try:
        return get(LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getLecturersURL",
            "query": name_part
        }).json()
    except Exception:
        return None

def get_lecturers_schedule(lecturer_id: str, TYPE: ScheduleType, weekday: str = None, is_next: bool = False) -> [str]:
    try:
        response: [{str, str}] = get(url=LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": TYPE.value,
            "prepodLogin": lecturer_id
        }).json()
    except Exception:
        return None
    
    if not response: return []
    
    if TYPE is ScheduleType.CLASSES:
        return beautify_lecturers_classes(response, is_next)
    elif TYPE is ScheduleType.EXAMS:
        return beautify_lecturers_exams(response)
