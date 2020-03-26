from aiogram.types import Message

from bot import dispatcher
from bot import students
from bot import metrics

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
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
    
    exams_schedule: [str] = students[message.chat.id].get_schedule(TYPE=ScheduleType.EXAMS)
    
    if exams_schedule is None: message_text: str = ResponseError.NO_RESPONSE.value
    elif len(exams_schedule) == 0: message_text: str = ResponseError.NO_DATA.value
    else: message_text: str = exams_schedule
    
    await loading_message.edit_text(
        text=message_text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
