from bot import bot
from bot import students

from bot.commands.classes.utilities.keyboards import weekday_chooser

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ClassesOptionType
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekType
from bot.shared.commands import Commands

from datetime import datetime
from random import choice


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.CLASSES.value and
        ClassesOptionType.DAILY.value in callback.data
)
@top_notification
def daily(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (weektype, weekday) = callback.data.split()[1:]
    
    schedule = students[callback.message.chat.id].get_schedule(
        TYPE=ScheduleType.CLASSES,
        is_next=weektype == WeekType.NEXT.value
    )
    
    if schedule is None: message_text = ResponseError.NO_RESPONSE.value
    elif len(schedule) == 0: message_text = ResponseError.NO_DATA.value
    else: message_text = schedule[int(weekday)]
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=message_text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].guard.drop()

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.CLASSES.value and
        ClassesOptionType.WEEKDAYS.value in callback.data
)
@top_notification
def certain_date_schedule(callback):
    weektype = callback.data.split()[1]
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=weekday_chooser(is_next=weektype == WeekType.NEXT.value)
    )
