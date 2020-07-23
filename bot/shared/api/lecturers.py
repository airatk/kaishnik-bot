from bot.shared.api.helpers import beautify_lecturers_classes
from bot.shared.api.helpers import beautify_lecturers_exams
from bot.shared.api.constants import LECTURERS_SCHEDULE_URL
from bot.shared.api.types import ScheduleType

from requests import get
from requests.exceptions import ConnectionError

from json.decoder import JSONDecodeError


def get_lecturers_names() -> [{str, str}]:
    try:
        return get(LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getLecturersURL",
            "query": "_"  # Underscore symbol to get all the names
        }).json()
    except (ConnectionError, JSONDecodeError):
        return None

def get_lecturers_schedule(lecturer_id: str, TYPE: ScheduleType, weektype: str = None, settings: object = None) -> [str]:
    try:
        response: [{str, str}] = get(url=LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": TYPE.value,
            "prepodLogin": lecturer_id
        }).json()
    except (ConnectionError, JSONDecodeError):
        return None
    
    if not response:
        return []
    
    if TYPE is ScheduleType.CLASSES:
        return beautify_lecturers_classes(response, weektype, settings)
    
    if TYPE is ScheduleType.EXAMS:
        return beautify_lecturers_exams(response, settings)
