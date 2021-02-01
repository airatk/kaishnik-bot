from random import choice

from typing import Optional
from typing import List

from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.student import get_group_schedule_id
from bot.utilities.api.student import get_schedule_by_group_schedule_id


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.EXAMS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.EXAMS.value ]
)
@increment_command_metrics(command=Commands.EXAMS)
async def exams(message: Message):
    loading_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    exams_arguments: List[str] = message.text.split()[1:]
    another_group_schedule_id: Optional[str] = None
    
    if len(exams_arguments) != 0:
        (another_group_schedule_id, response_error) = get_group_schedule_id(group=exams_arguments[0])
        
        if another_group_schedule_id is None:
            await loading_message.edit_text(
                text="\n".join([
                    "Расписание экзаменов группы *{group}* получить не удалось.".format(group=exams_arguments[0]),
                    response_error.value
                ]),
                parse_mode="markdown"
            )
            return
    
    (schedule, response_error) = get_schedule_by_group_schedule_id(
        schedule_type=ScheduleType.EXAMS,
        user_id=Users.get(Users.telegram_id == message.chat.id).user_id,
        another_group_schedule_id=another_group_schedule_id
    )
    
    await loading_message.edit_text(
        text=response_error.value if schedule is None else schedule,
        parse_mode="markdown",
        disable_web_page_preview=True
    )
