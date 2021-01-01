from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS

from datetime import date


def is_week_even(day_date: date = date.today()) -> bool:
    return get_week_number(day_date=day_date) % 2 == 0

def get_week_number(day_date: date = date.today()) -> int:
    (current_year, current_week, _) = day_date.isocalendar()
    
    semester_1st_day = date(current_year, 2 if day_date.month < 8 else 9, 1)
    first_week = semester_1st_day.isocalendar()[1]
    
    return (0 if current_week == 53 else current_week) - first_week + (0 if semester_1st_day.isoweekday() == 7 else 1)


def weekday_date() -> (str, str):
    day_date: date = date.today()
    weekday: int = day_date.isoweekday()
    
    return (
        WEEKDAYS[weekday] if weekday < 7 else "Воскресенье",
        "{day} {month}".format(
            day=int(day_date.strftime("%d")),  # int()-cast is used to replace "01 апреля" with "1 апреля"
            month=MONTHS[day_date.strftime("%m")]
        )
    )
