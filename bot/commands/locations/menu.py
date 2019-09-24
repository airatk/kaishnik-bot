from bot import bot
from bot import students
from bot import metrics

from bot.commands.locations.utilities.keyboards import location_type_chooser

from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.LOCATIONS.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.LOCATIONS)
def locations(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Аж 4 варианта на выбор:",
        reply_markup=location_type_chooser()
    )
    
    students[message.chat.id].guard.text = Commands.LOCATIONS.value
