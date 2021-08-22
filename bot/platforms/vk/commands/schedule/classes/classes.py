from random import choice

from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import states
from bot.platforms.vk import guards

from bot.platforms.vk.commands.schedule.utilities.keyboards import time_period_chooser
from bot.platforms.vk.commands.schedule.utilities.classes import common_show_chosen_date
from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.student import get_group_schedule_id


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize().startswith(CommandOfVK.CLASSES.value)
)
@note_metrics(platform=Platform.VK, command=Command.CLASSES)
async def menu(event: SimpleBotEvent):    
    classes_arguments: List[str] = event.text.split()[1:]
    
    if len(classes_arguments) != 0:
        await event.answer(
            message=choice(LOADING_REPLIES),
            dont_parse_links=True
        )
        
        (another_group_schedule_id, response_error) = get_group_schedule_id(group=classes_arguments[0])
        
        if another_group_schedule_id is None:
            await event.answer(
                message="\n".join([
                    "Расписание занятий группы {group} получить не удалось.".format(group=classes_arguments[0]),
                    response_error.value
                ]),
                keyboard=to_menu()
            )
            return
        
        states[event.peer_id].another_group_schedule_id = another_group_schedule_id
    
    await event.answer(
        message="Тебе нужно расписание{for_another_group} на:".format(
            for_another_group=" группы {group}".format(group=classes_arguments[0]) if len(classes_arguments) != 0 else ""
        ),
        keyboard=time_period_chooser()
    )

@vk_bot.message_handler(PayloadContainsFilter(key=Command.CLASSES_SHOW.value))
async def show_chosen_date(event: SimpleBotEvent):
    await common_show_chosen_date(command=Command.CLASSES, event=event)
