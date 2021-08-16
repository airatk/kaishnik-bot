from typing import List

from aiogram.types import Message
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.notes.utilities.keyboards import action_chooser

from bot.models.users import Users
from bot.models.notes import Notes

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.NOTES.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.NOTES.value ]
)
@increment_command_metrics(command=Commands.NOTES)
async def notes(message: Message):
    guards[message.chat.id].text = Commands.NOTES.value
    
    notes: List[Notes] = Notes.select().where(Notes.user_id == Users.get(Users.telegram_id == message.chat.id).user_id)
    
    await message.answer(
        text="Заметок всего: *{current}/{max}*".format(
            current=notes.count(),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=action_chooser(has_notes=notes.exists())
    )
