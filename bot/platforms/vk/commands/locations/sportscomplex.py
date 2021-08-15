from typing import List

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.locations.utilities.keyboards import sportscomplex_dialer
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.utilities.api.constants import SPORTSCOMPLEX
from bot.utilities.api.types import LocationType


@vk_bot.message_handler(PayloadFilter(payload={ "callback": LocationType.SPORTSCOMPLEX.value }))
async def sportscomplex(event: SimpleBotEvent):
    await event.answer(
        message="У родного КАИ 1 спортивный комплекс из 3 составляющих:",
        keyboard=sportscomplex_dialer()
    )

@vk_bot.message_handler(PayloadContainsFilter(key="sportscomplex"))
async def send_sportscomplex(event: SimpleBotEvent):
    numbers: List[int] = list(map(int, event.payload["sportscomplex"].split(",")))
    
    for number in numbers:
        await event.answer(
            lat=SPORTSCOMPLEX[number]["latitude"],
            long=SPORTSCOMPLEX[number]["longitude"],
            message="\n".join([
                SPORTSCOMPLEX[number]["title"],
                SPORTSCOMPLEX[number]["address"]
            ])
        )
        await event.answer(
            message=SPORTSCOMPLEX[number]["description"],
            keyboard=to_menu()
        )
