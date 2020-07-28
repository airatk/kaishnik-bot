from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.keyboards import cancel_button
from bot.shared.api.types import ClassesOptionType
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS
from bot.shared.calendar.types import WeekType

from datetime import datetime
from datetime import timedelta


def time_period_chooser(lecturer_id: str = "None") -> InlineKeyboardMarkup:
    time_period_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    # Decrementing to turn both variables into schedule array indices
    today_weekday: int = datetime.today().isoweekday() - 1
    
    tomorrow_weekday: int = today_weekday + 1
    yesterday_weekday: int = today_weekday - 1
    
    should_show_next_week: bool = tomorrow_weekday > 6
    should_show_previous_week: bool = yesterday_weekday < 0
    
    time_period_chooser_keyboard.add(*[
        cancel_button(),
        InlineKeyboardButton(
            text="сегодня",
            callback_data=" ".join([
                ClassesOptionType.DAY.value,
                WeekType.CURRENT.value,
                str(today_weekday),
                lecturer_id
            ])
        ),
        InlineKeyboardButton(
            text="вчера",
            callback_data=" ".join([
                ClassesOptionType.DAY.value,
                WeekType.PREVIOUS.value if should_show_previous_week else WeekType.CURRENT.value,
                "6" if should_show_previous_week else str(yesterday_weekday),
                lecturer_id
            ])
        ),
        InlineKeyboardButton(
            text="завтра",
            callback_data=" ".join([
                ClassesOptionType.DAY.value,
                WeekType.NEXT.value if should_show_next_week else WeekType.CURRENT.value,
                "0" if should_show_next_week else str(tomorrow_weekday),
                lecturer_id
            ])
        ),
        InlineKeyboardButton(
            text="неделю",
            callback_data=" ".join([ ClassesOptionType.WEEKTYPES.value, lecturer_id ])
        )
    ])
    
    return time_period_chooser_keyboard

def weektype_chooser(lecturer_id: str = "None") -> InlineKeyboardMarkup:
    weektype_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    weektype_chooser_keyboard.row(cancel_button())
    
    weektype_chooser_keyboard.add(*[
        InlineKeyboardButton(text="предыдущая", callback_data=" ".join([
            ClassesOptionType.WEEKDAYS.value, WeekType.PREVIOUS.value, lecturer_id
        ])),
        InlineKeyboardButton(text="текущая", callback_data=" ".join([
            ClassesOptionType.WEEKDAYS.value, WeekType.CURRENT.value, lecturer_id
        ])),
        InlineKeyboardButton(text="следующая", callback_data=" ".join([
            ClassesOptionType.WEEKDAYS.value, WeekType.NEXT.value, lecturer_id
        ]))
    ])
    
    return weektype_chooser_keyboard

def weekday_chooser(weektype: str, lecturer_id: str = "None") -> InlineKeyboardMarkup:
    weekday_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    weekday_chooser_keyboard.row(
        cancel_button(),
        InlineKeyboardButton(
            text="показать все",
            callback_data=" ".join([
                ClassesOptionType.WEEK.value,
                weektype,
                lecturer_id
            ])
        )
    )
    
    today_date: datetime = datetime.today()
    today_weekday: int = today_date.isoweekday()
    
    week_shift: int = 0
    
    if weektype == WeekType.NEXT.value: week_shift = 7
    elif weektype == WeekType.PREVIOUS.value: week_shift = -7
    
    for weekday in WEEKDAYS:
        day_date: datetime = today_date + timedelta(days=(weekday - today_weekday) + week_shift)
        
        weekday_chooser_keyboard.row(
            InlineKeyboardButton(
                text="{weekday}, {day} {month}{is_today}".format(
                    weekday=WEEKDAYS[weekday],
                    day=int(day_date.strftime("%d")), month=MONTHS[day_date.strftime("%m")],
                    is_today=" •" if today_date == day_date else ""
                ),
                callback_data=" ".join([
                    ClassesOptionType.DAY.value,
                    weektype,
                    str(weekday - 1),  # Decrementing to turn the variable into schedule array index
                    lecturer_id
                ])
            )
        )
    
    return weekday_chooser_keyboard
