from bot.shared.api.helpers import beautify_lecturers_classes
from bot.shared.api.helpers import beautify_lecturers_exams
from bot.shared.api.constants import LECTURERS_SCHEDULE_URL
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError

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

def get_lecturers_schedule(lecturer_id: str, TYPE: ScheduleType, dates: [str] = [], settings: object = None) -> [str]:
    try:
        response: [{str, str}] = get(url=LECTURERS_SCHEDULE_URL, params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": TYPE.value,
            "prepodLogin": lecturer_id
        }).json()
        
        if not response: raise Exception
    except (ConnectionError, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE.value)
    except Exception:
        return (None, ResponseError.NO_DATA.value)
    
    if TYPE is ScheduleType.CLASSES:
        return (beautify_lecturers_classes(raw_schedule=response, settings=settings, dates=dates), None)
    
    if TYPE is ScheduleType.EXAMS:
        return (beautify_lecturers_exams(raw_schedule=response, settings=settings), None)
