from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.locations.utilities.keyboards import libraries_dialer
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.utilities.helpers import remove_markdown
from bot.utilities.api.constants import BUILDINGS
from bot.utilities.api.constants import LIBRARIES
from bot.utilities.api.types import LocationType


@vk_bot.message_handler(PayloadFilter(payload={ "callback": LocationType.LIBRARY.value }))
async def libraries(event: SimpleBotEvent):
    await event.answer(
        message="У родного КАИ 5 библиотек:",
        keyboard=libraries_dialer()
    )

@vk_bot.message_handler(PayloadContainsFilter(key="library"))
async def send_library(event: SimpleBotEvent):
    numbers: List[int] = list(map(int, event.payload["library"].split(",")))
    
    for number in numbers:
        building: int = LIBRARIES[number]["building"] - 1
        
        await event.answer(
            lat=BUILDINGS[building]["latitude"],
            long=BUILDINGS[building]["longitude"],
            message="\n".join([
                LIBRARIES[number]["title"],
                BUILDINGS[building]["address"]
            ])
        )
        await event.answer(
            message=remove_markdown(LIBRARIES[number]["description"]),
            keyboard=to_menu()
        )
