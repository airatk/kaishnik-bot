from typing import Optional
from typing import List

from random import choice

from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.models.users import Users

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.student import get_group_schedule_id
from bot.utilities.api.student import get_schedule_by_group_schedule_id


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize().startswith(CommandsOfVK.EXAMS.value)
)
@increment_command_metrics(command=Commands.EXAMS)
async def exams(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    exams_arguments: List[str] = event.text.split()[1:]
    another_group_schedule_id: Optional[str] = None
    
    if len(exams_arguments) != 0:
        (another_group_schedule_id, response_error) = get_group_schedule_id(group=exams_arguments[0])
        
        if another_group_schedule_id is None:
            await event.answer(
                message="\n".join([
                    "Расписание экзаменов группы {group} получить не удалось.".format(group=exams_arguments[0]),
                    response_error.value
                ]),
                keyboard=to_menu
            )
            return
    
    (schedule, response_error) = get_schedule_by_group_schedule_id(
        schedule_type=ScheduleType.EXAMS,
        user_id=Users.get(Users.vk_id == event.peer_id).user_id,
        another_group_schedule_id=another_group_schedule_id
    )
    
    await event.answer(
        message=remove_markdown(response_error.value if schedule is None else schedule),
        dont_parse_links=True,
        keyboard=to_menu()
    )
