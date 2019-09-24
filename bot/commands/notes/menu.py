from bot import bot
from bot import students
from bot import metrics

from bot.commands.notes.utilities.keyboards import action_chooser
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.NOTES.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.NOTES)
def notes(message):
    students[message.chat.id].guard.text = Commands.NOTES.value
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[message.chat.id].notes),
            max=MAX_NOTES_NUMBER
        ),
        reply_markup=action_chooser(has_notes=len(students[message.chat.id].notes) != 0),
        parse_mode="Markdown"
    )
