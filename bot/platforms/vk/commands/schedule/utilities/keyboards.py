from typing import List
from typing import Dict
from typing import Union

from datetime import date
from datetime import timedelta

from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.keyboards import menu_button

from bot.utilities.types import Command
from bot.utilities.calendar.constants import WEEKDAYS
from bot.utilities.calendar.constants import MONTHS
from bot.utilities.calendar.helpers import get_semester_boundaries
from bot.utilities.calendar.helpers import is_week_even


def time_period_chooser(lecturer_id: str = "-") -> str:
    time_period_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    today_date: date = date.today()
    yesterday_date: date = today_date - timedelta(days=1)
    tomorrow_date: date = today_date + timedelta(days=1)

    command: str = Command.CLASSES_SHOW.value if lecturer_id == "-" else Command.LECTURERS_CLASSES_SHOW.value
    
    time_period_chooser_keyboard.add_text_button(**menu_button())
    time_period_chooser_keyboard.add_text_button(
        text="Сегодня", payload={
            command: "", 
            "date_string": today_date.strftime("%d.%m"), 
            "lecturer_id": lecturer_id 
        }
    )
    
    time_period_chooser_keyboard.add_row()
    time_period_chooser_keyboard.add_text_button(
        text="Вчера", payload={
            command: "", 
            "date_string": yesterday_date.strftime("%d.%m"), 
            "lecturer_id": lecturer_id 
        }
    )
    time_period_chooser_keyboard.add_text_button(
        text="Завтра", payload={ 
            command: "", 
            "date_string": tomorrow_date.strftime("%d.%m"), 
            "lecturer_id": lecturer_id
        }
    )

    later_date_text: str = ""
    later_dates: List[date] = [ 
        tomorrow_date + timedelta(days=days_number) 
        for days_number in range(1, 4) 
    ]
    later_dates = [ 
        later_date + timedelta(days=1 if later_date.isoweekday() == 7 else 0)
        for later_date in later_dates
    ]
    
    for later_date in later_dates:
        if later_date.isoweekday() == 1:
            later_date_text = f"{WEEKDAYS[later_date.isoweekday()]}, {'чётная' if is_week_even(day_date=later_date) else 'нечётная'}"
        else:
            later_date_text = f"{WEEKDAYS[later_date.isoweekday()]}, {later_date.day} {MONTHS[later_date.strftime('%m')]}"
        
        time_period_chooser_keyboard.add_row()
        time_period_chooser_keyboard.add_text_button(
            text=later_date_text, payload={ 
                command: "", 
                "date_string": later_date.strftime("%d.%m"), 
                "lecturer_id": lecturer_id
            }
        )
    
    time_period_chooser_keyboard.add_row()
    time_period_chooser_keyboard.add_text_button(
        text="Весь семестр", color=ButtonColor.SECONDARY, payload={ 
            command: "", 
            "lecturer_id": lecturer_id 
        }
    )
    
    return time_period_chooser_keyboard.get_keyboard()

def dates_scroller(shown_date_string: str, lecturer_id: str = "-") -> str:
    days_scroller_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    (first_date, last_date) = get_semester_boundaries(day_date=date.today())

    shown_date: date = date(date.today().year, *map(int, shown_date_string.split(".")[::-1]))
    earlier_date: date = shown_date - timedelta(days=(1 if shown_date.isoweekday != 1 else 2))
    later_date: date = shown_date + timedelta(days=(1 if shown_date.isoweekday != 6 else 2))

    # Shifting backwards for 7 days, because of the weirdness of university schedule for
    # if not first_date.month > 7:
    #     first_date -= timedelta(days=7)
    
    command: str = Command.CLASSES_SHOW.value if lecturer_id == "-" else Command.LECTURERS_CLASSES_SHOW.value

    movement_buttons: List[Dict[str, Union[str, Dict]]] = [ { 
            "text": "Раньше", 
            "payload": { 
                command: "",
                "date_string": earlier_date.strftime("%d.%m"),
                "lecturer_id": lecturer_id
            }
        }, {
            "text": "Позже", 
            "payload": { 
                command: "",
                "date_string": later_date.strftime("%d.%m"),
                "lecturer_id": lecturer_id
            }
        }
    ]
    
    if earlier_date < first_date:
        del movement_buttons[0]
    elif later_date > last_date:
        del movement_buttons[1]

    if len(movement_buttons) == 1:
        days_scroller_keyboard.add_text_button(**menu_button())

    for movement_button in movement_buttons:
        days_scroller_keyboard.add_text_button(**movement_button)
    
    if len(movement_buttons) > 1:
        days_scroller_keyboard.add_row()
        days_scroller_keyboard.add_text_button(**menu_button())
    
    return days_scroller_keyboard.get_keyboard()
