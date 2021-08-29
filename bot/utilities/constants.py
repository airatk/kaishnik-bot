from typing import List

from config import Config


KEYS_FILE: str = "data/keys"
KEYS: Config = Config(KEYS_FILE)


GROUP_NUMBER_PATTERN: str = "[0-9][0-9][0-9][0-9][0-9]?[0-9]?"

SUBJECTS_NUMBER: int = 4

MAX_NOTES_NUMBER: int = 40
MAX_SYMBOLS_NUMBER: int = 25


BRS: str = (
    "*БРС*\n"
    "_балльно-рейтинговая система_\n"
    "\n"
    "Обычно можно получить *50* баллов за семестр и столько же за экзамен. *100* баллов всего.\n"
    "\n"
    "• 3ка - от *51* до *70*\n"
    "• 4ка - от *71* до *85*\n"
    "• 5ка - от *86* до *100*\n"
    "\n"
    "Для зачёта достаточно получить *51* балл в сумме.\n"
)

DONATE: str = (
    "Если тебе понравился бот, ты можешь добровольно отблагодарить разработчика денежным донатом:\n"
    "\n"
    "• *Сбер*: 2202 2012 3023 9101\n"
    "• *PayPal*: paypal.me/kamairat\n"
    "\n"
    "{top_donators}"
    "Спасибо, что пользуешься ботом!☺️\n"
)

TOP_DONATORS_NUMBER: int = 6


PLATFORM_USER_INFO: str = (
    "{fullname}{username}\n"
    "chat id {chat_id}\n"
)

USER_BB_CREDENTIALS_INFO: str = (
    "Логин: {login}\n"
    "Пароль: {password}\n"
)

BASE_USER_INFO: str = (
    "Группа {group}\n"
    "\n"
    "• Заметок: {notes_number}\n"
)

COMPACT_USER_INFO: str = "\n".join([
    PLATFORM_USER_INFO,
    BASE_USER_INFO
])

BB_USER_INFO: str = "\n".join([
    PLATFORM_USER_INFO,
    USER_BB_CREDENTIALS_INFO,
    BASE_USER_INFO
])

USER_ID_MODIFIER: int = 999
DIGIT_MODIFIER: int = ord("e")
PLATFORM_CODE_SUFFIX: str = "-kaist"
POSSIBLE_PLATFORM_CODE_CHARACTERS: List[str] = [ chr(digit + DIGIT_MODIFIER) for digit in range(10) ]

PLATFORM_CODE_INFO: str = "Твой код для входа: `{platform_code}`"


REPLIES_TO_UNKNOWN_COMMAND: List[str] = [
    "Список команд можно увидеть, введя * / * (не отправляй! просто введи)",
    "Введи * / *, но не отправляй, и ты увидишь список поддерживаемых команд. А твою я не знаю🙅🏼‍♀️",
    "Я понимаю лишь определённые команды. Они доступны после ввода * / * (не отправляй, только введи)",
    "_«Не любая команда — команда»_ — [Создатель](https://telegram.me/airatk)."
]

REPLIES_TO_UNKNOWN_TEXT_MESSAGE: List[str] = [
    "Не понимаю!",
    "Не делай так, я отвечаю лишь на определённые команды.",
    "Если ты думаешь, что это весело — писать мне непонятные сообщения, то нет.",
    "Ўт тЅЁЅ! тЎЁы Ј тЅЁЅ ЁыЋЎ ­ЅЏЎ­ят­Ў!",
    "А может, ты лучше команду введёшь?",
    "_«Самолёт должен быть красивым, чтобы он полетел»_ — Андрей Николаевич Туполев.",
    "Я не умею отвечать на естественные сообщения — я же всего лишь глупый алгоритм.",
    "🙃",
    (
        "Пау, чика, пау-уау — я напева-а-ю;\n"
        "Мау-мау-мау, моё сердце страдает,\n"
        "Чики-чики-чуа-а, и сно-ва:\n"
        "Гичи-гичи-гу — значит, я люблю!"
    ),
    "🙅🏼‍♀️",
    "К чёрту всё! Я люблю тебя!😚",
    "Целовались студееенты, распускались тюльпаааны, чикчири-ка-ло там и тут… Ой, ты ещё здесь?",
    "_«Чудо нельзя в своих подвалах скрывать. Сложилось — надо на свет выпускать. »_"
]

REPLIES_TO_UNKNOWN_NONTEXT_MESSAGE: List[str] = [
    "Закодируй в ASCII и попробуй отправить текстом.",
    "Капча!😱 …или нет. Не понимаю."
]
