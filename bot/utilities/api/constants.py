from typing import List


# Directions to go for the data
SCHEDULE_URL: str = "https://kai.ru/raspisanie"
LECTURERS_SCHEDULE_URL: str = "https://kai.ru/for-staff/raspisanie"
SCORE_URL: str = "https://old.kai.ru/info/students/brs.php"

P_SUB: str = (
    "01100110011100100110111101101101011010110110000101101001011100"
    "1101101000011011100110100101101011011000100110111101110100011"
    "1011101101001011101000110100001101100011011110111011001100101"
)

LOADING_REPLIES: [str] = [
    "стучусь на сервера kai.ru…",
    "ожидание ответа от серверов kai.ru…"
]


INSTITUTES: {str: str} = {
    "1": "ИАНТЭ",
    "2": "ФМФ",
    "3": "ИАЭП",
    "4": "♥ ИКТЗИ ♥",
    "5": "ИРЭТ",
    "28": "ИЭУСТ"
}


FULL_CLASS_ENTITIES: List[str] = [
    "*[ {time} ][ {place} ]",
    "[ {dates} ]",
    "{title}*",
    "_{type}_"
]

COMPACT_CLASS_ENTITIES: List[str] = [
    "*{time} • {place}*",
    "({dates})",
    "*{type}:* {title}"
]

LECTURER_ENTITY: str = "@ {lecturer}"
DEPARTMENT_ENTITY: str = "§ {department}"

GROUPS_ENTITY: str = "• У группы {group}"


FULL_EXAM_ENTITIES: List[str] = [
    "*[ {date}, {time} ][ {building}ка, {auditorium} ]*",
    "*{title}*"
]

COMPACT_EXAM_ENTITIES: List[str] = [
    "*{date}, {time} • {building}ка, {auditorium}*",
    "{title}"
]
