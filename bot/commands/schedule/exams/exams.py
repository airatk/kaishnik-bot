from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.EXAMS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.EXAMS.value ]
)
@metrics.increment(Commands.EXAMS)
async def exams(message: Message):
    loading_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    request_entities: [str] = message.text.split()
    
    if len(request_entities) > 1:
        students[message.chat.id].another_group = request_entities[1]
        
        if students[message.chat.id].another_group_schedule_id is None:
            await loading_message.edit_text(
                text="Расписание экзаменов группы *{group}* получить не удалось :(".format(group=request_entities[1]),
                parse_mode="markdown"
            )
            
            students[message.chat.id].guard.drop()
            return
    
    (schedule, error_message) = students[message.chat.id].get_schedule(TYPE=ScheduleType.EXAMS)
    
    await loading_message.edit_text(
        text=error_message if schedule is None else schedule,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
