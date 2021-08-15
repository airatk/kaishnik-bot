from typing import List

from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.locations.utilities.keyboards import sportscomplex_dialer
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.types import Commands
from bot.utilities.api.constants import SPORTSCOMPLEX
from bot.utilities.api.types import LocationType


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOCATIONS.value and
        callback.data == LocationType.SPORTSCOMPLEX.value
)
@top_notification
async def sportscomplex(callback: CallbackQuery):
    await callback.message.edit_text(
        text="У родного КАИ 1 спортивный комплекс из 3 составляющих:",
        reply_markup=sportscomplex_dialer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOCATIONS.value and
        LocationType.SPORTSCOMPLEX.value in callback.data
)
@top_notification
async def send_sportscomplex(callback: CallbackQuery):
    await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    numbers: List[int] = list(map(int, callback.data.split()[1].split(",")))
    
    await callback.message.delete()
    
    for number in numbers:
        await callback.message.answer_venue(
            latitude=SPORTSCOMPLEX[number]["latitude"],
            longitude=SPORTSCOMPLEX[number]["longitude"],
            title=SPORTSCOMPLEX[number]["title"],
            address=SPORTSCOMPLEX[number]["address"]
        )
        await callback.message.answer(
            text=SPORTSCOMPLEX[number]["description"]
        )
    
    guards[callback.message.chat.id].drop()
