from telebot.types import CallbackQuery

from bot import bot
from bot import students

from bot.commands.locations.utilities.keyboards import libraries_dialer
from bot.commands.locations.utilities.constants import BUILDINGS
from bot.commands.locations.utilities.constants import LIBRARIES
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.LIBRARY.value
)
@top_notification
def libraries(callback: CallbackQuery):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 5 библиотек:",
        reply_markup=libraries_dialer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.LIBRARY.value in callback.data
)
@top_notification
def send_library(callback: CallbackQuery):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number: str = callback.data.split()[1]
    building: str = LIBRARIES[number]["building"]
    
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[building]["latitude"],
        longitude=BUILDINGS[building]["longitude"],
        title=LIBRARIES[number]["title"],
        address=BUILDINGS[building]["address"]
    )
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=LIBRARIES[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
