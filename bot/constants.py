# kaishnik-bot constants
from os import environ
TOKEN   = environ["T_TOKEN"]
CREATOR = int(environ["T_CREATOR"])

# Directions to go in for the main data
SCHEDULE_URL           = "https://kai.ru/raspisanie"
SCORE_URL              = "http://old.kai.ru/info/students/brs.php"
LECTURERS_SCHEDULE_URL = "https://kai.ru/for-staff/raspisanie"

# Official emoji list of the Unicode Consortium: http://unicode.org/emoji/charts/full-emoji-list.html
EMOJI = {
    "smirking":    "\U0001F60F", # 😏
    "smiling":     "\U0001F642", # 🙂
    "upside-down": "\U0001F643", # 🙃
    "kissing":     "\U0001F61A", # 😚
    "crying":      "\U0001F622", # 😢
    "no-woman":    "\U0001F645", # 🙅‍♀️
    "moon":        "\U0001F31A", # 🌚
    "heart":       "\U00002665"  # ♥️
}

# Week
WEEK = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота"
}

# Institutes
INSTITUTES = {
    "ИАНТЭ": "1",
    "ФМФ":   "2",
    "ИАЭП":  "3",
    EMOJI["heart"] + " ИКТЗИ " + EMOJI["heart"]: "4",
    "КИТ":   "КИТ",
    "ИРЭТ":  "5",
    "ИЭУСТ": "28"
}

# Locations
BUILDINGS = {
    "1": {
        "description": "*Первый дом*\n\n"
                       "Ближайшая остановка: КАИ.\n"
                       "Есть буфет и читальный зал №1.",
        "latitude":  55.7971077,
        "longitude": 49.1129913
    },
    "2": {
        "description": "*2ка*\n\n"
                       "Ближайшие остановки: Четаева, Чистопольская, Амирхана, СК Олимп.\n"
                       "Есть буфет.",
        "latitude":  55.8226860,
        "longitude": 49.1360610
    },
    "3": {
        "description": "*3ка*\n\n"
                       "Ближайшие остановки: Толстого и Гоголя.\n"
                       "Есть буфет и читальный зал №3.",
        "latitude":  55.7918200,
        "longitude": 49.1374140
    },
    "4": {
        "description": "*4ка*\n\n"
                       "Ближайшие остановки: Толстого и Гоголя.\n"
                       "Ни буфета, ни читального зала - грустно!",
        "latitude":  55.7931629,
        "longitude": 49.1374294
    },
    "5": {
        "description": "*5ка*\n\n"
                       "Ближайшая остановка: Площадь Свободы.\n"
                       "Есть столовая и читальный зал №2.",
        "latitude":  55.7969110,
        "longitude": 49.1237459
    },
    "6": {
        "description": "*6ка*\n\n"
                       "Ближайшие остановки: Институт, Кошевого, КМПО.\n"
                       "Есть буфет.",
        "latitude":  55.8542530,
        "longitude": 49.0980440
    },
    "7": {
        "description": "*7ка*\n\n"
                       "Ближайшие остановки: Гоголя и Толстого.\n"
                       "Есть буфет и читальный зал №9.",
        "latitude":  55.7971410,
        "longitude": 49.1345289
    },
    "8": {
        "description": "*8ка*\n\n"
                       "Ближайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.\n"
                       "Есть буфет и научно-техническая библиотека.",
        "latitude":  55.8208035,
        "longitude": 49.1363205
    },
    "СК Олимп": {
        "description": "*СК Олимп*\n\n"
                       "Ближайшие остановки: СК Олимп, Чистопольская, Четаева, Амирхана.\n"
                       "На самом деле, у Олимпа два здания: основное и здание бассейна, а ещё есть стадион.",
        "latitude":  55.8201111,
        "longitude": 49.1398743
    }
}

LIBRARIES = {
    "1": {
        "description": "*Читальный зал №1*\n\n"
                       "Ближайшая остановка: КАИ.\n"
                       "В первом доме.",
        "building": "1"
    },
    "2": {
        "description": "*Читальный зал №2*\n\n"
                       "Ближайшая остановка: Площадь Свободы.\n"
                       "В 5ке.",
        "building": "5"
    },
    "3": {
        "description": "*Читальный зал №3*\n\n"
                       "Ближайшие остановки: Толстого и Гоголя.\n"
                       "В 3ке.",
        "building": "3"
    },
    "9": {
        "description": "*Читальный зал №9*\n\n"
                       "Ближайшие остановки: Гоголя и Толстого.\n"
                       "В 7ке.",
        "building": "7"
    },
    "научно-техническая": {
        "description": "*Научно-техническая библиотека*\n\n"
                       "Ближайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.\n"
                       "В 8ке.",
        "building": "8"
    }
}

DORMS = {
    "1": {
        "description": "*Первое общежитие*\n\n"
                       "Ближайшая остановка: КАИ.",
        "latitude":  55.7984276,
        "longitude": 49.1154430
    },
    "2": {
        "description": "*Второе общежитие*\n\n"
                       "Ближайшая остановка: КАИ.\n"
                       "Есть столовая.",
        "latitude":  55.7978831,
        "longitude": 49.1147940
    },
    "3": {
        "description": "*Третье общежитие*\n\n"
                       "Ближайшие остановки: Попова, Пионерская, Губкина, ТД Риф Эль.\n"
                       "Есть столовая.",
        "latitude":  55.8095929,
        "longitude": 49.1998827
    },
    "4": {
        "description": "*Четвёртое общежитие*\n\n"
                       "Ближайшие остановки: Солнышко, Короленко, Октябрьская, Голубятникова.",
        "latitude":  55.8379590,
        "longitude": 49.1009150
    },
    "5": {
        "description": "*Пятое общежитие*\n\n"
                       "Ближайшие остановки: Абжалилова, Кооперативный институт, Патриса Лумумбы, парк Горького.\n"
                       "Есть столовая.",
        "latitude":  55.7927011,
        "longitude": 49.1644210
    },
    "6": {
        "description": "*Шестое общежитие*\n\n"
                       "Ближайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
        "latitude":  55.7851918,
        "longitude": 49.1559488
    },
    "7": {
        "description": "*Седьмое общежитие*\n\n"
                       "Ближайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
        "latitude":  55.7853090,
        "longitude": 49.1549720
    }
}

# /brs
BRS = "*БРС*\n" \
      "_балльно-рейтинговая система_\n\n" \
      "Обычно можно получить *50* баллов за семестр и столько же за экзамен. *100* баллов всего.\n\n"\
      "• 3ка - от *51* до *70*\n" \
      "• 4ка - от *71* до *85*\n" \
      "• 5ка - от *86* до *100*\n\n" \
      "Для зачёта достаточно получить *51* балл в сумме.\n\n" \
      "_варьируется от преподавателя к преподавателю_"

# Creator's commands
CREATOR_COMMAND = "*Safe commands*\n" \
                  "/metrics\n" \
                  "/users\n" \
                  "/clear\n" \
                  "\n*Unsafe commands*\n" \
                  "/ drop\n" \
                  "/ broadcast _text_\n" \
                  "/ reverseweek\n" \
                  "\n*Hashtags*\n" \
                  "#users\n" \
                  "#erased\n" \
                  "#dropped\n" \
                  "#ТелеграммаОтРазработчика"

# Replies to unknow stuff
REPLIES_TO_UNKNOWN_COMMAND = [
    "Список команд можно увидеть, введя * / * (но не отправляя!).",
    "Введи * / *, но не отправляй, и ты увидишь поддерживаемые команды. А твою я не знаю" + EMOJI["no-woman"],
    "Я понимаю лишь несколько команд. Они доступны после ввода * / * (не отправлять, только ввести).",
    "_\"Не любая команда - команда\"_ - [Создатель](https://telegram.me/airatk)."
]

REPLIES_TO_UNKNOWN_MESSAGE = [
    "Не понимаю!",
    "Не делай так, я отвечаю лишь на определённые команды.",
    "Если ты думаешь, что это весело - писать мне непонятные сообщения, то нет.",
    "Ўт тЅЁЅ! тЎЁы Ј тЅЁЅ ЁыЋЎ ­ЅЏЎ­ят­Ў!",
    "А может, ты лучше команду введёшь?",
    "_\"Самолёт должен быть красивым, чтобы он полетел.\"_",
    "Я не умею отвечать на естественные сообщения - я же всего лишь глупый алгоритм.",
    EMOJI["upside-down"],
    EMOJI["no-woman"],
    "К чёрту всё! Я люблю тебя!" + EMOJI["kissing"],
    "Введи * / * - увидишь список поддерживаемых команд.",
    "Целовались студееенты, распускались тюльпаааны, чикчири-ка-ло там и тут... Ой, ты ещё здесь?",
    "Список команд можно увидеть, введя * / * (но не отправляя!).",
    "Я понимаю лишь несколько команд. Они доступны после ввода * / * (не отправлять, только ввести)."
]
