from aiogram.types import CallbackQuery

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.locations.utilities.keyboards import libraries_dialer
from bot.commands.locations.utilities.constants import BUILDINGS
from bot.commands.locations.utilities.constants import LIBRARIES
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.LIBRARY.value
)
@top_notification
async def libraries(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 5 библиотек:",
        reply_markup=libraries_dialer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.LIBRARY.value in callback.data
)
@top_notification
async def send_library(callback: CallbackQuery):
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number: str = callback.data.split()[1]
    building: str = LIBRARIES[number]["building"]
    
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[building]["latitude"],
        longitude=BUILDINGS[building]["longitude"],
        title=LIBRARIES[number]["title"],
        address=BUILDINGS[building]["address"]
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LIBRARIES[number]["description"]
    )
    
    students[callback.message.chat.id].guard.drop()
