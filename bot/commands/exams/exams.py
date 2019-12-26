from aiogram.types import Message

from bot import bot
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
    loading_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    request_entities: [str] = message.text.split()
    
    if len(request_entities) > 1:
        students[message.chat.id].another_group = request_entities[1]
        
        if students[message.chat.id].another_group is None:
            await bot.edit_message_text(
                chat_id=loading_message.chat.id,
                message_id=loading_message.message_id,
                text="Расписание экзаменов группы *{group}* получить не удалось :(".format(group=request_entities[1])
            )
            
            students[message.chat.id].guard.drop()
            return
    
    exams: [str] = students[message.chat.id].get_schedule(TYPE=ScheduleType.EXAMS)
    
    if exams is None: message_text: str = ResponseError.NO_RESPONSE.value
    elif len(exams) == 0: message_text: str = ResponseError.NO_DATA.value
    else: message_text: str = exams
    
    await bot.edit_message_text(
        chat_id=loading_message.chat.id,
        message_id=loading_message.message_id,
        text=message_text,
        disable_web_page_preview=True
    )
