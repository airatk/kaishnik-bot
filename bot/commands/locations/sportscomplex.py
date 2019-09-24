from bot import bot
from bot import students

from bot.commands.locations.utilities.keyboards import sportscomplex_dialer
from bot.commands.locations.utilities.constants import SPORTSCOMPLEX
from bot.commands.locations.utilities.types import LocationType

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        callback.data == LocationType.SPORTSCOMPLEX.value
)
@top_notification
def s_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 1 спортивный комплекс из 3 составляющих:",
        reply_markup=sportscomplex_dialer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOCATIONS.value and
        LocationType.SPORTSCOMPLEX.value in callback.data
)
@top_notification
def send_sportscomplex(callback):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number = " ".join(callback.data.split()[1:])
    
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    bot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=SPORTSCOMPLEX[number]["latitude"],
        longitude=SPORTSCOMPLEX[number]["longitude"],
        title=SPORTSCOMPLEX[number]["title"],
        address=SPORTSCOMPLEX[number]["address"]
    )
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=SPORTSCOMPLEX[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()
