from datetime import date
from datetime import timedelta

from typing import Tuple

from bot.utilities.calendar.constants import WEEKDAYS
from bot.utilities.calendar.constants import MONTHS


def is_week_even(day_date: date) -> bool:
    return get_week_number(day_date=day_date) % 2 == 0

def get_week_number(day_date: date) -> int:
    semester_first_day: date = get_semester_boundaries(day_date=day_date)[0]
    semester_first_week: int = semester_first_day.isocalendar()[1]
    current_week: int = day_date.isocalendar()[1]
    
    return (current_week if day_date.month == 1 and current_week < 52 else 0) - semester_first_week + (0 if semester_first_day.isoweekday() == 7 else 1)


def get_semester_boundaries(day_date: date) -> Tuple[date, date]:
    if day_date.month > 7:
        first_date: date = date(day_date.year, 9, 1)
        last_date: date = date(day_date.year, 12, 31)
    else:
        first_date: date = date(day_date.year, 2, 9)
        last_date: date = date(day_date.year, 6, 30)
        
        if first_date.isoweekday() > 4:
            first_date += timedelta(days=7 - first_date.isoweekday() + 1)
    
    return (first_date, last_date)


def weekday_date() -> Tuple[str, str]:
    day_date: date = date.today()
    weekday: int = day_date.isoweekday()
    
    return (
        WEEKDAYS[weekday] if weekday < 7 else "Воскресенье",
        "{day} {month}".format(
            day=day_date.strftime("%-d"),
            month=MONTHS[day_date.strftime("%m")]
        )
    )
