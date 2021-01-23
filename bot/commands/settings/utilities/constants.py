TELEGRAM_USER_INFO: str = (
    "{fullname}{username}\n"
    "chat id {chat_id}\n"
)

BASE_USER_INFO: str = (
    "• Заметок: {notes_number}\n"
)


GROUP_OF_STUDENTS_INFO: str = "\n".join([
    TELEGRAM_USER_INFO, (
        "Группа {group}\n"
    ),
    BASE_USER_INFO
])

COMPACT_STUDENT_INFO: str = "\n".join([
    TELEGRAM_USER_INFO, (
        "Группа {group}\n"
    ),
    BASE_USER_INFO
])

EXTENDED_STUDENT_INFO: str = "\n".join([
    TELEGRAM_USER_INFO, (
        "{institute}, {year} курс\n"
        "Группа {group}\n"
        "{name}\n"
        "\n"
        "Номер студенческого билета и зачётной книжки: {card}\n"
    ),
    BASE_USER_INFO
])

BB_STUDENT_INFO: str = "\n".join([
    TELEGRAM_USER_INFO, (
        "Логин: {login}\n"
        "Пароль: ********\n"
    ),
    BASE_USER_INFO
])
