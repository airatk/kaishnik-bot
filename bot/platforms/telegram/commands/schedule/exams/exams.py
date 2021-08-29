from typing import Optional
from typing import List

from random import choice

from aiogram.types import Message
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.student import get_group_schedule_id
from bot.utilities.api.student import get_schedule_by_group_schedule_id


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.EXAMS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.EXAMS.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.EXAMS)
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
                parse_mode=ParseMode.MARKDOWN
            )
            return
    
    (schedule, response_error) = get_schedule_by_group_schedule_id(
        schedule_type=ScheduleType.EXAMS,
        user_id=User.get(User.telegram_id == message.chat.id).user_id,
        another_group_schedule_id=another_group_schedule_id
    )
    
    await loading_message.edit_text(
        text=response_error.value if schedule is None else schedule,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
