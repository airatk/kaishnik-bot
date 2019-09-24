from bot import bot
from bot import students
from bot import metrics

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ResponseError
from bot.shared.commands import Commands

from random import choice


@bot.message_handler(
    commands=[ Commands.EXAMS.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.EXAMS)
def exams(message):
    loading_message = bot.send_message(
        chat_id=message.chat.id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    request_entities = message.text.split()
    
    if len(request_entities) > 1:
        students[message.chat.id].another_group = request_entities[1]
        
        if students[message.chat.id].another_group is None:
            bot.edit_message_text(
                chat_id=loading_message.chat.id,
                message_id=loading_message.message_id,
                text="Расписание экзаменов для группы *{group}* получить не удалось :(".format(group=request_entities[1]),
                parse_mode="Markdown"
            )
            
            students[message.chat.id].guard.drop()
            return
    
    exams = students[message.chat.id].get_schedule(TYPE=ScheduleType.EXAMS)
    
    if exams is None: message_text = ResponseError.NO_RESPONSE.value
    elif exams == []: message_text = ResponseError.NO_DATA.value
    else: message_text = exams
    
    bot.edit_message_text(
        chat_id=loading_message.chat.id,
        message_id=loading_message.message_id,
        text=message_text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
