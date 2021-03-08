from datetime import datetime

from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands
from bot.utilities.calendar.helpers import is_week_even
from bot.utilities.calendar.helpers import weekday_date
from bot.utilities.calendar.helpers import get_week_number


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.WEEK.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.WEEK.value ]
)
@increment_command_metrics(command=Commands.WEEK)
async def week(message: Message):
    (weekday, date) = weekday_date()
    
    week_number: int = get_week_number(day_date=datetime.today())
    
    if week_number > 0:
        week_message: str = (
            "Текущая неделя *{type}*,\n"
            "*#{number}* с начала семестра.".format(
                type="чётная" if is_week_even(day_date=datetime.today()) else "нечётная",
                number=week_number
            )
        )
    else:
        week_number = 1 - week_number
        
        week_message: str = "До начала семестра меньше *{week_number}* недел{ending}.".format(
            week_number=week_number,
            ending="и" if week_number == 1 else "ь"
        )
    
    await message.answer(
        text="\n\n".join([
            "*{weekday}, {date}*".format(weekday=weekday, date=date),
            week_message
        ]),
        parse_mode="markdown"
    )
