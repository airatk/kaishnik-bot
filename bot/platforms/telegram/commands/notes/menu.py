from peewee import ModelSelect

from aiogram.types import Message
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.notes.utilities.keyboards import action_chooser

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.NOTES.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.NOTES.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.NOTES)
async def notes(message: Message):
    guards[message.chat.id].text = Command.NOTES.value
    
    user: User = User.get(User.telegram_id == message.chat.id)
    user_notes: ModelSelect = Note.select().where(Note.user == user)
    
    await message.answer(
        text="Заметок всего: *{current}/{max}*".format(
            current=user_notes.count(),
            max=MAX_NOTES_NUMBER
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=action_chooser(has_notes=user_notes.exists())
    )
