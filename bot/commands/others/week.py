from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.shared.calendar.week import is_even
from bot.shared.calendar.week import weekday_date
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.WEEK.value ]
)
@metrics.increment(Commands.WEEK)
async def week(message: Message):
    (weekday, date) = weekday_date()
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=(
            "{weekday}, {date}.\n"
            "Текущая неделя *{type}*.".format(
                weekday=weekday, date=date,
                type="чётная" if is_even() else "нечётная"
            )
        )
    )
