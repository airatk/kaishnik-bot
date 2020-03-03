from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students

from bot.commands.classes.utilities.keyboards import weekday_chooser

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ClassesOptionType
from bot.shared.api.types import ResponseError
from bot.shared.calendar.week import WeekType
from bot.shared.commands import Commands

from random import choice


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.CLASSES.value and
        ClassesOptionType.DAILY.value in callback.data
)
@top_notification
async def daily(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (weektype, weekday) = callback.data.split()[1:]
    
    schedule: [str] = students[callback.message.chat.id].get_schedule(
        TYPE=ScheduleType.CLASSES,
        is_next=weektype == WeekType.NEXT.value
    )
    
    if schedule is None: message_text: str = ResponseError.NO_RESPONSE.value
    elif len(schedule) == 0: message_text: str = ResponseError.NO_DATA.value
    else: message_text: str = schedule[int(weekday)]
    
    await callback.message.edit_text(
        text=message_text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].guard.drop()

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.CLASSES.value and
        ClassesOptionType.WEEKDAYS.value in callback.data
)
@top_notification
async def certain_date_schedule(callback: CallbackQuery):
    weektype: str = callback.data.split()[1]
    
    await callback.message.edit_text(
        text="Выбери нужный день:",
        reply_markup=weekday_chooser(is_next=weektype == WeekType.NEXT.value)
    )
