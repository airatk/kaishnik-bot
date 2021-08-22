from typing import List

from aiogram.types import CallbackQuery

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.locations.utilities.keyboards import dorms_dialer
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.types import Command
from bot.utilities.api.constants import DORMS
from bot.utilities.api.types import LocationType


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LOCATIONS.value and
        callback.data == LocationType.DORM.value
)
@top_notification
async def dorms(callback: CallbackQuery):
    await callback.message.edit_text(
        text="У родного КАИ 7 общежитий:",
        reply_markup=dorms_dialer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LOCATIONS.value and
        LocationType.DORM.value in callback.data
)
@top_notification
async def send_dorm(callback: CallbackQuery):
    await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    numbers: List[int] = list(map(int, callback.data.split()[1].split(",")))
    
    await callback.message.delete()
    
    for number in numbers:
        await callback.message.answer_venue(
            latitude=DORMS[number]["latitude"],
            longitude=DORMS[number]["longitude"],
            title=DORMS[number]["title"],
            address=DORMS[number]["address"]
        )
        await callback.message.answer(
            text=DORMS[number]["description"]
        )
    
    guards[callback.message.chat.id].drop()
