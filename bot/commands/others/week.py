from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.shared.calendar.helpers import is_even
from bot.shared.calendar.helpers import weekday_date
from bot.shared.calendar.helpers import get_week_number
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.WEEK.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.WEEK.value ]
)
@metrics.increment(Commands.WEEK)
async def week(message: Message):
    (weekday, date) = weekday_date()
    
    week_number: int = get_week_number()
    
    if week_number > 0:
        week_message: str = (
            "Текущая неделя *{type}*,\n"
            "*#{number}* с начала семестра.".format(
                type="чётная" if is_even() else "нечётная",
                number=week_number
            )
        )
    else:
        week_number = -week_number + 1
        
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
