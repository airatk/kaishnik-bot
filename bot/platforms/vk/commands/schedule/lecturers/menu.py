from bot.utilities.api.types import ScheduleType
from typing import Dict
from typing import List

from random import choice

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards
from bot.platforms.vk import states

from bot.platforms.vk.commands.schedule.lecturers.utilities.keyboards import lecturer_chooser
from bot.platforms.vk.commands.schedule.lecturers.utilities.keyboards import lecturer_info_type_chooser
from bot.platforms.vk.commands.schedule.lecturers.utilities.constants import MAX_LECTURERS_NUMBER

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.keyboards import canceler
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.lecturers import get_lecturers_names


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.LECTURERS.value
)
@increment_command_metrics(command=Commands.LECTURERS)
async def lecturers(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    (lecturers_names, response_error) = get_lecturers_names()
    
    if lecturers_names is None:
        await event.answer(
            message=response_error.value,
            dont_parse_links=True,
            keyboard=to_menu()
        )
        return
    
    states[event.peer_id].lecturers_names = lecturers_names
    
    await event.answer(
        message="Отправь фамилию или ФИО преподавателя.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Commands.LECTURERS_NAME.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Commands.LECTURERS_NAME.value
)
async def find_lecturer(event: SimpleBotEvent):
    partial_name_parts: List[str] = event.text.lower().split(" ")
    names: List[Dict[str, str]] = list(filter( 
        lambda name: all([ partial_name_part in name["lecturer"].lower() for partial_name_part in partial_name_parts ]),
        states[event.peer_id].lecturers_names
    ))

    if len(names) == 0:
        await event.answer(
            message=(
                "Ничего не найдено :(\n\n"
                "Попробуешь ещё раз?"
            ),
            keyboard=canceler()
        )
        return
    
    if len(names) > MAX_LECTURERS_NUMBER:
        await event.answer(
            message=(
                "Слишком мало букв, слишком много преподавателей…\n\n"
                "Попробуешь ещё раз?"
            ),
            keyboard=canceler()
        )
        return
    
    await event.answer(
        message="Выбери преподавателя:",
        keyboard=lecturer_chooser(names=names)
    )

    guards[event.peer_id].text = Commands.LECTURERS.value

@vk_bot.message_handler(
    PayloadContainsFilter(key=Commands.LECTURERS.value),
    ~PayloadContainsFilter(key=ScheduleType.CLASSES.value),
    ~PayloadContainsFilter(key=ScheduleType.EXAMS.value)
)
async def lecturers_schedule_type(event: SimpleBotEvent):
    lecturer_id: str = event.payload["lecturer_id"]

    names: List[str] = list(filter(
        lambda lecturer: lecturer["id"] == lecturer_id,
        states[event.peer_id].lecturers_names
    ))
    chosen_name: str = names[0]["lecturer"].replace(" ", "\n", 1)
    
    states[event.peer_id].drop()

    await event.answer(message=chosen_name)
    await event.answer(
        message="Тебе нужны преподавателевы:",
        keyboard=lecturer_info_type_chooser(lecturer_id=lecturer_id)
    )
