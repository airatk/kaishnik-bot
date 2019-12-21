from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.shared.api.types import ClassesOptionType
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS
from bot.shared.calendar.week import WeekType

from datetime import datetime
from datetime import timedelta


def schedule_type() -> InlineKeyboardMarkup:
    schedule_type_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    
    # Decrementing to turn both variables into schedule array indeces
    today_weekday: int = datetime.today().isoweekday() - 1
    tomorrow_weekday: int = today_weekday + 1
    should_show_next_week: bool = tomorrow_weekday > 6
    
    schedule_type_keyboard.row(
        InlineKeyboardButton(text="сегодня",
            callback_data=" ".join([ ClassesOptionType.DAILY.value, WeekType.CURRENT.value, str(today_weekday) ])
        ),
        InlineKeyboardButton(text="завтра",
            callback_data=" ".join([
                ClassesOptionType.DAILY.value,
                WeekType.NEXT.value if should_show_next_week else WeekType.CURRENT.value,
                str(0 if should_show_next_week else tomorrow_weekday)
            ])
        )
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю",
        callback_data=" ".join([ ClassesOptionType.WEEKDAYS.value, WeekType.CURRENT.value ])
    ))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю",
        callback_data=" ".join([ ClassesOptionType.WEEKDAYS.value, WeekType.NEXT.value ])
    ))
    
    return schedule_type_keyboard


def weekday_chooser(is_next: bool) -> InlineKeyboardMarkup:
    weekday_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    
    weekday_chooser_keyboard.row(InlineKeyboardButton(text="Показать все",
        callback_data=" ".join([
            ClassesOptionType.WEEKLY.value,
            WeekType.NEXT.value if is_next else WeekType.CURRENT.value
        ])
    ))
    
    today: datetime = datetime.today()
    today_weekday: int = today.isoweekday()
    
    for weekday in WEEKDAYS:
        date: datetime = today + timedelta(days=(weekday - today_weekday) + (7 if is_next else 0))
        
        weekday_chooser_keyboard.row(
            InlineKeyboardButton(
                text="{weekday}, {day} {month}{is_today}".format(
                    weekday=WEEKDAYS[weekday],
                    day=int(date.strftime("%d")), month=MONTHS[date.strftime("%m")],
                    is_today=" •" if today == date else ""
                ),
                callback_data=" ".join([
                    ClassesOptionType.DAILY.value,
                    WeekType.NEXT.value if is_next else WeekType.CURRENT.value,
                    str(weekday - 1)  # Decrementing to turn the variable into schedule array index
                ])
            )
        )
    
    return weekday_chooser_keyboard
