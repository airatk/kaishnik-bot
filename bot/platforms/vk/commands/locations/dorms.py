from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.locations.utilities.keyboards import dorms_dialer
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.utilities.api.constants import DORMS
from bot.utilities.api.types import LocationType


@vk_bot.message_handler(PayloadFilter(payload={ "callback": LocationType.DORM.value }))
async def dorms(event: SimpleBotEvent):
    await event.answer(
        message="У родного КАИ 7 общежитий:",
        keyboard=dorms_dialer()
    )

@vk_bot.message_handler(PayloadContainsFilter(key="dorm"))
async def send_dorm(event: SimpleBotEvent):
    numbers: List[int] = list(map(int, event.payload["dorm"].split(",")))
    
    for number in numbers:
        await event.answer(
            lat=DORMS[number]["latitude"],
            long=DORMS[number]["longitude"],
            message="\n".join([
                DORMS[number]["title"],
                DORMS[number]["address"]
            ])
        )
        await event.answer(
            message=DORMS[number]["description"],
            keyboard=to_menu()
        )
