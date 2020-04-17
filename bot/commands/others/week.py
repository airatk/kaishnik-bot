from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.shared.calendar.week import is_even
from bot.shared.calendar.week import weekday_date
from bot.shared.calendar.week import get_week_number
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
    
    await message.answer(
        text=(
            "*{weekday}, {date}*\n"
            "\n"
            "Текущая неделя *{type}*,\n"
            "*#{number}* с начала семестра.".format(
                weekday=weekday, date=date,
                type="чётная" if is_even() else "нечётная",
                number=get_week_number()
            )
        ),
        parse_mode="markdown"
    )
