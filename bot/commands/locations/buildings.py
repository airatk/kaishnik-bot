from telebot.types import CallbackQuery

from bot import bot
from bot import students

from bot.commands.locations.utilities.keyboards import buildings_dialer
from bot.commands.locations.utilities.constants import BUILDINGS
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.BUILDING.value
)
@top_notification
def buildings(callback: CallbackQuery):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 8 учебных зданий:",
        reply_markup=buildings_dialer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.BUILDING.value in callback.data
)
@top_notification
def send_building(callback: CallbackQuery):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number: str = callback.data.split()[1]
    
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[number]["latitude"],
        longitude=BUILDINGS[number]["longitude"],
        title=BUILDINGS[number]["title"],
        address=BUILDINGS[number]["address"]
    )
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=BUILDINGS[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
