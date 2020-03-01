from aiogram.types import CallbackQuery

from bot import dispatcher

from bot import students

from bot.commands.locations.utilities.keyboards import dorms_dialer
from bot.commands.locations.utilities.constants import DORMS
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
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
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.DORM.value in callback.data
)
@top_notification
async def send_dorm(callback: CallbackQuery):
    await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number: str = callback.data.split()[1]
    
    await callback.message.delete()
    await callback.message.answer_venue(
        latitude=DORMS[number]["latitude"],
        longitude=DORMS[number]["longitude"],
        title=DORMS[number]["title"],
        address=DORMS[number]["address"]
    )
    await message.answer(text=DORMS[number]["description"])
    
    students[callback.message.chat.id].guard.drop()
