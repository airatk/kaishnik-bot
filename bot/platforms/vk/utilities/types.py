from enum import Enum


class CommandOfVK(Enum):
    START = "Start"
    RESTART = "Start"

    LOGIN_NEW_USER = "Войти как новый пользователь"
    LOGIN_VIA_TELEGRAM = "Войти через Телеграм"

    LOGIN_BB = "По логину-паролю от ББ"
    LOGIN_COMPACT = "По номеру группы"

    MENU = "Меню"
    MORE = "Ещё"

    CLASSES = "Занятия"
    LECTURERS = "Преподаватели"
    EXAMS = "Экзамены"
    SCORE = "Баллы"

    NOTES = "Заметки"

    LOCATIONS = "Здания КАИ"

    WEEK = "Неделя"
    BRS = "БРС"
    HELP = "Подсказки"
    DONATE = "Сказать спасибо"

    SETTINGS = "Настройки"

    CANCEL = "Отменить"
    CONTINUE = "Продолжить"
