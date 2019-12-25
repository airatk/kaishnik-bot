from aiogram.types import CallbackQuery

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.locations.utilities.keyboards import buildings_dialer
from bot.commands.locations.utilities.constants import BUILDINGS
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.BUILDING.value
)
@top_notification
async def buildings(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 8 учебных зданий:",
        reply_markup=buildings_dialer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.BUILDING.value in callback.data
)
@top_notification
async def send_building(callback: CallbackQuery):
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number: str = callback.data.split()[1]
    
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[number]["latitude"],
        longitude=BUILDINGS[number]["longitude"],
        title=BUILDINGS[number]["title"],
        address=BUILDINGS[number]["address"]
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=BUILDINGS[number]["description"]
    )
    
    students[callback.message.chat.id].guard.drop()
