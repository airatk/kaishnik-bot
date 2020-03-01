from aiogram.types import Message

from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.edit.utilities.keyboards import action_chooser

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.EDIT.value ]
)
@metrics.increment(Commands.EDIT)
async def edit(message: Message):
    edited_number: int = len(students[message.chat.id].edited_subjects)
    
    await message.answer(
        text="Отредактировано пар: *{edited_number}*".format(edited_number=edited_number),
        parse_mode="markdown",
        reply_markup=action_chooser(has_edits=edited_number != 0)
    )
    
    students[message.chat.id].guard.text = Commands.EDIT.value
