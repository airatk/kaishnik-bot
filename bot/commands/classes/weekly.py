from aiogram.types import CallbackQuery

from bot import bot
from bot import dispatcher

from bot import students

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ClassesOptionType
from bot.shared.api.types import ResponseError
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekType
from bot.shared.commands import Commands

from random import choice


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.CLASSES.value and
        ClassesOptionType.WEEKLY.value in callback.data
)
@top_notification
async def weekly_schedule(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    weektype: str = callback.data.split()[1]
    
    schedule: [str] = students[callback.message.chat.id].get_schedule(
        TYPE=ScheduleType.CLASSES,
        is_next=weektype == WeekType.NEXT.value
    )
    
    if schedule is None:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
    elif len(schedule) == 0:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_DATA.value,
            disable_web_page_preview=True
        )
    else:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        for weekday in WEEKDAYS:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=schedule[weekday - 1]
            )
    
    students[callback.message.chat.id].guard.drop()
