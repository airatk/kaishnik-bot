from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.locations.utilities.keyboards import buildings_dialer
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.utilities.api.constants import BUILDINGS
from bot.utilities.api.types import LocationType


@vk_bot.message_handler(PayloadFilter(payload={ "callback": LocationType.BUILDING.value }))
async def buildings(event: SimpleBotEvent):
    await event.answer(
        message="У родного КАИ 8 учебных зданий:",
        keyboard=buildings_dialer()
    )

@vk_bot.message_handler(PayloadContainsFilter(key="building"))
async def send_building(event: SimpleBotEvent):
    numbers: List[int] = list(map(int, event.payload["building"].split(",")))
    
    for number in numbers:
        await event.answer(
            lat=BUILDINGS[number]["latitude"],
            long=BUILDINGS[number]["longitude"],
            message="\n".join([
                BUILDINGS[number]["title"],
                BUILDINGS[number]["address"]
            ])
        )
        await event.answer(
            message=BUILDINGS[number]["description"],
            keyboard=to_menu()
        )
