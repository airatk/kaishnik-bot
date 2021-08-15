from datetime import date
from datetime import timedelta

from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.commands.schedule.utilities.constants import INITIAL_SHIFT
from bot.platforms.telegram.commands.schedule.utilities.constants import MOVEMENT_SHIFT
from bot.platforms.telegram.commands.schedule.utilities.constants import DATES_NUMBER

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.utilities.types import Commands
from bot.utilities.calendar.helpers import get_semester_boundaries
from bot.utilities.calendar.helpers import is_week_even
from bot.utilities.calendar.constants import WEEKDAYS
from bot.utilities.calendar.constants import MONTHS


def time_period_chooser(lecturer_id: str = "-") -> InlineKeyboardMarkup:
    time_period_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    today_date: date = date.today()
    yesterday_date: date = today_date - timedelta(days=1)
    tomorrow_date: date = today_date + timedelta(days=1)
    
    time_period_chooser_keyboard.add(*[
        cancel_button(),
        InlineKeyboardButton(text="сегодня", callback_data=" ".join([ Commands.CLASSES_SHOW.value, today_date.strftime("%d.%m"), lecturer_id ])),
        InlineKeyboardButton(text="вчера", callback_data=" ".join([ Commands.CLASSES_SHOW.value, yesterday_date.strftime("%d.%m"), lecturer_id ])),
        InlineKeyboardButton(text="завтра", callback_data=" ".join([ Commands.CLASSES_SHOW.value, tomorrow_date.strftime("%d.%m"), lecturer_id ]))
    ])
    
    time_period_chooser_keyboard.row(
        InlineKeyboardButton(
            text="другие дни",
            callback_data=" ".join([ Commands.CLASSES_CHOOSE.value, str(INITIAL_SHIFT), "", lecturer_id ])
        )
    )
    time_period_chooser_keyboard.row(
        InlineKeyboardButton(
            text="весь семестр",
            callback_data=" ".join([ Commands.CLASSES_SHOW.value, "", lecturer_id ])
        )
    )
    
    return time_period_chooser_keyboard

def dates_appender(shift: int, dates: List[str], lecturer_id: str = "-") -> InlineKeyboardMarkup:
    dates_appender_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    (first_date, last_date) = get_semester_boundaries(day_date=date.today())

    # Shifting backwards for 7 days, because of the weirdness of university schedule
    if not first_date.month > 7:
        first_date -= timedelta(days=7)
    
    if (date.today() - first_date).days < 0 and shift < (first_date - date.today()).days:
        shift = (first_date - date.today()).days
    elif (date.today() - last_date).days > 0:
        shift = (last_date - date.today()).days - abs(INITIAL_SHIFT) - MOVEMENT_SHIFT
    
    day_date: date = date.today() + timedelta(days=shift - (1 if date.today().isoweekday() == 1 else 0))
    weekday: int = day_date.isoweekday()
    
    for _ in range(DATES_NUMBER):
        if weekday == 7 and day_date != date.today():
            day_date += timedelta(days=1)
            weekday = 1
        elif day_date < first_date:
            day_date += timedelta(days=1)
            weekday = day_date.isoweekday()
        
        if day_date < first_date: continue
        if day_date > last_date: break
        
        raw_day: str = day_date.strftime("%d")
        raw_month: str = day_date.strftime("%m")
        raw_date: str = ".".join([ raw_day, raw_month ])
        
        text: str = "Сегодня" if day_date == date.today() else WEEKDAYS[weekday]
        
        if weekday == 1:
            text = ", ".join([ text, "чётная" if is_week_even(day_date=day_date) else "нечётная" ])
        elif day_date != date.today():
            text = "{text}, {day} {month}".format(text=text, day=int(raw_day), month=MONTHS[raw_month])
        
        dates_appender_keyboard.row(InlineKeyboardButton(
            text="".join([ text, " •" if raw_date in dates else "" ]),
            callback_data=" ".join([ Commands.CLASSES_CHOOSE.value, str(shift), raw_date, lecturer_id ])
        ))
        
        day_date += timedelta(days=1)
        weekday = day_date.isoweekday()
    
    movement_buttons: List[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text="раньше",
            callback_data=" ".join([ Commands.CLASSES_CHOOSE.value, str(shift - MOVEMENT_SHIFT), "", lecturer_id ])
        ),
        InlineKeyboardButton(
            text="позже",
            callback_data=" ".join([ Commands.CLASSES_CHOOSE.value, str(shift + MOVEMENT_SHIFT), "", lecturer_id ])
        )
    ]
    
    if (first_date - date.today()).days >= shift:
        del movement_buttons[0]
    elif (last_date - date.today()).days < (shift + abs(INITIAL_SHIFT) + MOVEMENT_SHIFT):
        del movement_buttons[1]
    
    dates_appender_keyboard.add(*movement_buttons)
    
    if len(dates) == 0:
        dates_appender_keyboard.row(cancel_button())
    else:
        dates_appender_keyboard.add(*[
            cancel_button(),
            InlineKeyboardButton(
                text="показать".format(chosen_dates_number=len(dates)),
                callback_data=" ".join([ Commands.CLASSES_SHOW.value, "", lecturer_id ])
            )
        ])
    
    return dates_appender_keyboard
