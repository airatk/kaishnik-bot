from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.commands.schedule.utilities.constants import INITIAL_SHIFT
from bot.commands.schedule.utilities.constants import MOVEMENT_SHIFT

from bot.shared.keyboards import cancel_button
from bot.shared.api.types import ClassesOptionType
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS

from datetime import date
from datetime import timedelta


def time_period_chooser(lecturer_id: str = "None") -> InlineKeyboardMarkup:
    time_period_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    today: date = date.today()
    yesterday: date = today - timedelta(days=1)
    tomorrow: date = today + timedelta(days=1)
    
    today_date: str = ".".join([ today.strftime("%d"), today.strftime("%m") ])
    yesterday_date: str = ".".join([ yesterday.strftime("%d"), yesterday.strftime("%m") ])
    tomorrow_date: str = ".".join([ tomorrow.strftime("%d"), tomorrow.strftime("%m") ])
    
    time_period_chooser_keyboard.add(*[
        cancel_button(),
        
        InlineKeyboardButton(text="сегодня", callback_data=" ".join([ ClassesOptionType.SHOW.value, today_date, lecturer_id ])),
        InlineKeyboardButton(text="вчера", callback_data=" ".join([ ClassesOptionType.SHOW.value, yesterday_date, lecturer_id ])),
        InlineKeyboardButton(text="завтра", callback_data=" ".join([ ClassesOptionType.SHOW.value, tomorrow_date, lecturer_id ]))
    ])
    
    time_period_chooser_keyboard.row(
        InlineKeyboardButton(text="другие дни", callback_data=" ".join([ ClassesOptionType.CHOOSE.value, str(INITIAL_SHIFT), "", lecturer_id ]))
    )
    time_period_chooser_keyboard.row(
        InlineKeyboardButton(text="весь семестр", callback_data=" ".join([ ClassesOptionType.SHOW.value, "", lecturer_id ]))
    )
    
    return time_period_chooser_keyboard

def dates_appender(shift: int, dates: [str], lecturer_id: str = "None") -> InlineKeyboardMarkup:
    dates_appender_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    dates_number: int = 7
    date_index: int = 0
    
    if date.today().month < 8:
        first_date: str = date(date.today().year, 2, 1)
        last_date: str = date(date.today().year, 6, 30)
    else:
        first_date: str = date(date.today().year, 9, 1)
        last_date: str = date(date.today().year, 12, 31)
    
    while date_index < dates_number:
        date_index += 1
        
        day_date: date = date.today() + timedelta(days=date_index + shift)
        
        if day_date < first_date: continue
        if day_date > last_date: break
        
        weekday: int = day_date.isoweekday()
        
        if weekday == 7:
            dates_number += 1
            continue
        
        raw_day: str = day_date.strftime("%d")
        raw_month: str = day_date.strftime("%m")
        raw_date: str = ".".join([ raw_day, raw_month ])
        
        text: str = "Сегодня" if (date_index + shift) == 0 else "{weekday}, {day} {month}".format(
            weekday=WEEKDAYS[weekday], day=int(raw_day), month=MONTHS[raw_month]
        )
        
        dates_appender_keyboard.row(InlineKeyboardButton(
            text="".join([ text, " •" if raw_date in dates else "" ]),
            callback_data=" ".join([ ClassesOptionType.CHOOSE.value, str(shift), raw_date, lecturer_id ])
        ))
    
    movement_buttons: [InlineKeyboardButton] = [
        InlineKeyboardButton(
            text="раньше", callback_data=" ".join([ ClassesOptionType.CHOOSE.value, str(shift - MOVEMENT_SHIFT), "", lecturer_id ])
        ),
        InlineKeyboardButton(
            text="позже", callback_data=" ".join([ ClassesOptionType.CHOOSE.value, str(shift + MOVEMENT_SHIFT), "", lecturer_id ])
        )
    ]
    
    if (first_date - date.today()).days >= (shift + INITIAL_SHIFT): del movement_buttons[0]
    if (last_date - date.today()).days <= (shift - INITIAL_SHIFT + MOVEMENT_SHIFT + 1): del movement_buttons[1]
    
    dates_appender_keyboard.add(*movement_buttons)
    
    if len(dates) == 0:
        dates_appender_keyboard.row(cancel_button())
    else:
        dates_appender_keyboard.add(*[
            cancel_button(),
            InlineKeyboardButton(
                text="показать".format(chosen_dates_number=len(dates)),
                callback_data=" ".join([ ClassesOptionType.SHOW.value, "", lecturer_id ])
            )
        ])
    
    return dates_appender_keyboard
