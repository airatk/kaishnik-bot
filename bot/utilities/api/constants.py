from typing import List
from typing import Dict
from typing import Union


# HTTP-request constants
SCHEDULE_URL: str = "https://kai.ru/raspisanie"
LECTURERS_SCHEDULE_URL: str = "https://kai.ru/for-staff/raspisanie"

CAS_LOGIN_URL: str = "https://cas.kai.ru:8443/cas/login"
CAS_SERVICE_LOGIN_URL: str = "https://cas.kai.ru:8443/cas/login?service=https://kai.ru/c/portal/login"
STUDENT_DATA_URL: str = "https://kai.ru/group/guest/student/{data_type}"

LOADING_REPLIES: List[str] = [
    "Стучусь на сервера kai.ru…",
    "Ожидание ответа от серверов kai.ru…"
]

AUTH_TOKEN_SIGN: str = "Liferay.authToken = '"
AUTH_TOKEN_LENGTH: int = 8


# UI constants
FULL_CLASS_ENTITIES: List[str] = [
    "*[ {time} ][ {place} ]*",
    "*[ {dates} ]*",
    "*{title}*",
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

SCORE_TEMPLATE: str = (
    "*{}*\n"
    "\n"
    "• 1 аттестация: {} / {}\n"
    "• 2 аттестация: {} / {}\n"
    "• 3 аттестация: {} / {}\n"
    "• 4 аттестация: {} / {}\n"
    "• 5 аттестация: {} / {}\n"
    "\n"
    "• Предварительная оценка: {}\n"
    "• Дополнительные баллы: {}\n"
    "\n"
    "• Долги: {}\n"
    "\n"
    "• Окончательная оценка: {}\n"
    "• Традиционная оценка: *{}*"
)


# Locations data constants
BUILDINGS: List[Dict[str, Union[str, int]]] = [
    {
        "button": "1",
        "title": "Первое учебное здание",
        "description": (
            "• Есть буфет и читальный зал №1.\n"
            "• Ближайшая остановка: КАИ."
        ),
        "address": "Карла Маркса, 10",
        "latitude": 55.7971077,
        "longitude": 49.1129913
    }, {
        "button": "2",
        "title": "Второе учебное здание",
        "description": (
            "• Есть буфет.\n"
            "• Ближайшие остановки: Четаева, Чистопольская, Амирхана, СК Олимп."
        ),
        "address": "Четаева, 18",
        "latitude": 55.8226860,
        "longitude": 49.1360610
    }, {
        "button": "3",
        "title": "Третье учебное здание",
        "description": (
            "• Есть буфет и читальный зал №3.\n"
            "• Ближайшие остановки: Толстого и Гоголя."
        ),
        "address": "Толстого, 15",
        "latitude": 55.7918200,
        "longitude": 49.1374140
    }, {
        "button": "4",
        "title": "Четвёртое учебное здание",
        "description": (
            "• Ни буфета, ни читального зала — грустно!\n"
            "• Ближайшие остановки: Толстого и Гоголя."
        ),
        "address": "Горького, 28/17",
        "latitude": 55.7931629,
        "longitude": 49.1374294
    }, {
        "button": "5",
        "title": "Пятое учебное здание",
        "description": (
            "• Есть столовая и читальный зал №2.\n"
            "• Ближайшая остановка: Площадь Свободы."
        ),
        "address": "Карла Маркса, 31/7",
        "latitude": 55.7969110,
        "longitude": 49.1237459
    }, {
        "button": "6",
        "title": "Шестое учебное здание",
        "description": (
            "• Есть буфет.\n"
            "• Ближайшие остановки: Институт, Кошевого, КМПО."
        ),
        "address": "Дементьева, 2а",
        "latitude": 55.8542530,
        "longitude": 49.0980440
    }, {
        "button": "7",
        "title": "Седьмое учебное здание",
        "description": (
            "• Есть буфет и читальный зал №9.\n"
            "• Ближайшие остановки: Гоголя и Толстого."
        ),
        "address": "Большая Красная, 55",
        "latitude": 55.7971410,
        "longitude": 49.1345289
    }, {
        "button": "8",
        "title": "Восьмое учебное здание",
        "description": (
            "• Есть буфет и научно-техническая библиотека.\n"
            "• Ближайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана."
        ),
        "address": "Четаева, 18а",
        "latitude": 55.8208035,
        "longitude": 49.1363205
    }
]

LIBRARIES: List[Dict[str, Union[str, int]]] = [
    {
        "button": "1",
        "title": "Читальный зал №1",
        "description": "*В 1ке.* Ближайшая остановка: КАИ.",
        "building": 1
    }, {
        "button": "2",
        "title": "Читальный зал №2",
        "description": "*В 5ке.* Ближайшая остановка: Площадь Свободы.",
        "building": 5
    }, {
        "button": "3",
        "title": "Читальный зал №3",
        "description": "*В 3ке.* Ближайшие остановки: Толстого и Гоголя.",
        "building": 3
    }, {
        "button": "9",
        "title": "Читальный зал №9",
        "description": "*В 7ке.* Ближайшие остановки: Гоголя и Толстого.",
        "building": 7
    }, {
        "button": "научно-техническая",
        "title": "Научно-техническая",
        "description": "*В 8ке.* Ближайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.",
        "building": 8
    }
]

SPORTSCOMPLEX: List[Dict[str, Union[str, int]]] = [
    {
        "button": "Главное здание",
        "title": "Главное здание",
        "description": "Ближайшие остановки: СК Олимп, Чистопольская, Четаева, Амирхана.",
        "address": "Чистопольская, 65",
        "latitude": 55.8201111,
        "longitude": 49.1398743
    }, {
        "button": "Здание бассейна",
        "title": "Здание бассейна",
        "description": "Ближайшие остановки: СК Олимп, Чистопольская, Четаева, Амирхана.",
        "address": "Чистопольская, 65",
        "latitude": 55.821139,
        "longitude": 49.1402243
    }, {
        "button": "Стадион",
        "title": "Стадион",
        "description": "Ближайшие остановки: СК Олимп, Чистопольская, Четаева, Амирхана.",
        "address": "Чистопольская, 65",
        "latitude": 55.821703,
        "longitude": 49.140717
    }
]

DORMS: List[Dict[str, Union[str, int]]] = [
    {
        "button": "1",
        "title": "Первое общежитие",
        "description": "Ближайшая остановка: КАИ.",
        "address": "Большая Красная, 7/9",
        "latitude": 55.7984276,
        "longitude": 49.1154430
    }, {
        "button": "2",
        "title": "Второе общежитие",
        "description": (
            "• Есть столовая.\n"
            "• Ближайшая остановка: КАИ."
        ),
        "address": "Большая Красная, 18",
        "latitude": 55.7978831,
        "longitude": 49.1147940
    }, {
        "button": "3",
        "title": "Третье общежитие",
        "description": (
            "• Есть столовая.\n"
            "• Ближайшие остановки: Попова, Пионерская, Губкина, Арбузова, Национальный архив."
        ),
        "address": "Кирпичникова, 11",
        "latitude": 55.8095929,
        "longitude": 49.1998827
    }, {
        "button": "4",
        "title": "Четвёртое общежитие",
        "description": "Ближайшие остановки: Солнышко, Короленко, Октябрьская, Голубятникова.",
        "address": "Короленко, 85",
        "latitude": 55.8379590,
        "longitude": 49.1009150
    }, {
        "button": "5",
        "title": "Пятое общежитие",
        "description": (
            "• Есть столовая."
            "• Ближайшие остановки: Абжалилова, Кооперативный институт, Патриса Лумумбы, парк Горького."
        ),
        "address": "Ершова, 30",
        "latitude": 55.7927011,
        "longitude": 49.1644210
    }, {
        "button": "6",
        "title": "Шестое общежитие",
        "description": "Ближайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
        "address": "Товарищеская, 30",
        "latitude": 55.7851918,
        "longitude": 49.1559488
    }, {
        "button": "7",
        "title": "Седьмое общежитие",
        "description": "Ближайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
        "address": "Товарищеская, 30а",
        "latitude": 55.7853090,
        "longitude": 49.1549720
    }
]
