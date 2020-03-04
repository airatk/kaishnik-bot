FULL_USER_INFO: str = (
    "{firstname}{lastname}{username}\n"
    "chat id {chat_id}\n\n"
    "{institute}, {year} курс\n"
    "Группа {group_number}\n"
    "{name}\n\n"
    "• Номер зачётки: {card}\n\n"
    "• Заметок: {notes_number}\n"
    "• Изменений в расписании: {edited_classes_number}"
)

COMPACT_USER_INFO: str = (
    "{firstname}{lastname}{username}\n"
    "chat id {chat_id}\n\n"
    "• Группа {group_number}\n\n"
    "• Заметок: {notes_number}\n"
    "• Изменений в расписании: {edited_classes_number}"
)
