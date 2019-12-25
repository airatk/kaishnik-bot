from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.notes.utilities.keyboards import action_chooser
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.NOTES.value ]
)
@metrics.increment(Commands.NOTES)
async def notes(message: Message):
    students[message.chat.id].guard.text = Commands.NOTES.value
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[message.chat.id].notes),
            max=MAX_NOTES_NUMBER
        ),
        reply_markup=action_chooser(has_notes=len(students[message.chat.id].notes) != 0)
    )
