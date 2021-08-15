from random import choice

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.users import Users

from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.lecturers import get_lecturers_schedule


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Commands.LECTURERS.value,
    PayloadContainsFilter(key=ScheduleType.EXAMS.value)
)
async def lecturers_exams(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )

    lecturer_id: str = event.payload["lecturer_id"]
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    
    (schedule, response_error) = get_lecturers_schedule(
        lecturer_id=lecturer_id,
        schedule_type=ScheduleType.EXAMS,
        user_id=user_id
    )
    
    await event.answer(
        message=remove_markdown(response_error.value if schedule is None else schedule),
        dont_parse_links=True,
        keyboard=to_menu()
    )

    guards[event.peer_id].drop()
