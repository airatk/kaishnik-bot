from telebot.types import Message

from bot import bot
from bot import students
from bot import metrics

from bot.shared.calendar.week import is_even
from bot.shared.calendar.week import weekday_date
from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.WEEK.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.WEEK)
def week(message: Message):
    (weekday, date) = weekday_date()
    
    bot.send_message(
        chat_id=message.chat.id,
        text=(
            "{weekday}, {date}.\n"
            "Текущая неделя *{type}*.".format(
                weekday=weekday, date=date,
                type="чётная" if is_even() else "нечётная"
            )
        ),
        parse_mode="Markdown"
    )
