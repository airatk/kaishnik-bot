from aiogram.types import Message

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.notes.utilities.keyboards import action_chooser
from bot.commands.notes.utilities.constants import MAX_NOTES_NUMBER

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.NOTES.value ]
)
@metrics.increment(Commands.NOTES)
async def notes(message: Message):
    students[message.chat.id].guard.text = Commands.NOTES.value
    
    await message.answer(
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[message.chat.id].notes),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode="markdown",
        reply_markup=action_chooser(has_notes=len(students[message.chat.id].notes) != 0)
    )
