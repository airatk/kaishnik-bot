from bot import bot
from bot import students

from bot.commands.locations.utilities.keyboards import dorms_dialer
from bot.commands.locations.utilities.constants import DORMS
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.DORM.value
)
@top_notification
def dorms(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 7 общежитий:",
        reply_markup=dorms_dialer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.DORM.value in callback.data
)
@top_notification
def send_dorm(callback):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number = callback.data.split()[1]
    
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=DORMS[number]["latitude"],
        longitude=DORMS[number]["longitude"],
        title=DORMS[number]["title"],
        address=DORMS[number]["address"]
    )
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=DORMS[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
