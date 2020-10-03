from bot.shared.data.constants import USERS_FILE
from bot.shared.data.constants import USERS_JSON

from pickle import load
from pickle import dump

from json import dump as json_dump


def save_data(file: str, data: object) -> None:
    with open(file, "wb") as opened_file:
        dump(data, opened_file, protocol=4)

def load_data(file: str) -> {str: object}:
    with open(file, "rb") as opened_file:
        return load(opened_file)


def get_users_data() -> object:
    return open(USERS_FILE, "rb")

def get_users_json() -> object:
    users: {str: object} = load_data(file=USERS_FILE)
    
    users = { chat_id: {
        "setup": {
            "is_setup": student.is_setup,
            "type": "none" if student.type is None else student.type.value
        },
        "institute": {
            "institute": student.institute,
            "institute_id": student.institute_id
        },
        "year": student.year,
        "group": {
            "group": student._group,
            "group_schedule_id": student.group_schedule_id,
            "group_score_id": student.group_score_id
        },
        "name": {
            "name": student.name,
            "name_id": student.name_id
        },
        "card": student.card,
        "notes": student.notes,
        "settings": {
            "is_schedule_size_full": student.settings.is_schedule_size_full,
            "are_classes_on_dates": student.settings.are_classes_on_dates
        }
    } for (chat_id, student) in users.items() }
    
    with open(USERS_JSON, "w") as json_file:
        json_dump(users, json_file, indent=4, ensure_ascii=False)
    
    return open(USERS_JSON, "r")
