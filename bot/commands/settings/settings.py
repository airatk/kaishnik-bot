from aiogram.types import Message
from aiogram.types import Chat
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.settings.utilities.keyboards import action_chooser
from bot.commands.settings.utilities.constants import FULL_USER_INFO
from bot.commands.settings.utilities.constants import COMPACT_USER_INFO

from bot.shared.commands import Commands
from bot.shared.api.student import Student


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.SETTINGS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.SETTINGS.value ]
)
@metrics.increment(Commands.SETTINGS)
async def settings(message: Message):
    chat: Chat = await message.bot.get_chat(chat_id=message.chat.id)
    
    info: {str: str} = {
        "fullname": chat.full_name,
        "username": " @{username}".format(username=chat.username) if chat.username is not None else "",
        "chat_id": message.chat.id if message.chat.type == ChatType.PRIVATE else (-message.chat.id - 1_000_000_000_000),
        "group": students[message.chat.id].group,
        "notes_number": len(students[message.chat.id].notes),
        "edited_classes_number": len(students[message.chat.id].edited_subjects)
    }
    
    await message.answer(
        text=FULL_USER_INFO.format(
            **info,
            institute=students[message.chat.id].institute[2:-2],  # Removing emojis
            year=students[message.chat.id].year,
            name=students[message.chat.id].name,
            card=students[message.chat.id].card
        ) if students[message.chat.id].type is Student.Type.EXTENDED else COMPACT_USER_INFO.format(**info),
        reply_markup=action_chooser()
    )
    
    students[message.chat.id].guard.text = Commands.SETTINGS.value
