from aiogram.types import CallbackQuery

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.locations.utilities.keyboards import sportscomplex_dialer
from bot.commands.locations.utilities.constants import SPORTSCOMPLEX
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.SPORTSCOMPLEX.value
)
@top_notification
async def s_s(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 1 спортивный комплекс из 3 составляющих:",
        reply_markup=sportscomplex_dialer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.SPORTSCOMPLEX.value in callback.data
)
@top_notification
async def send_sportscomplex(callback: CallbackQuery):
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number: str = " ".join(callback.data.split()[1:])
    
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=SPORTSCOMPLEX[number]["latitude"],
        longitude=SPORTSCOMPLEX[number]["longitude"],
        title=SPORTSCOMPLEX[number]["title"],
        address=SPORTSCOMPLEX[number]["address"]
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=SPORTSCOMPLEX[number]["description"]
    )
    
    students[callback.message.chat.id].guard.drop()
