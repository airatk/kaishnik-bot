from aiogram.types import Chat
from aiogram.types import Message

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import FULL_USER_INFO
from bot.commands.others.utilities.constants import COMPACT_USER_INFO

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.SETTINGS.value ]
)
@metrics.increment(Commands.SETTINGS)
async def settings(message: Message):
    chat: Chat = await message.bot.get_chat(chat_id=message.chat.id)
    
    if students[message.chat.id].is_full:
        message_text = FULL_USER_INFO.format(
            firstname=chat.first_name,
            lastname=f" {chat.last_name}" if chat.last_name is not None else "",
            username=f" @{chat.username}" if chat.username is not None else "",
            chat_id=message.chat.id,
            institute=students[message.chat.id].institute,
            year=students[message.chat.id].year,
            group_number=students[message.chat.id].group,
            name=students[message.chat.id].name,
            card=students[message.chat.id].card,
            notes_number=len(students[message.chat.id].notes),
            edited_classes_number=len(students[message.chat.id].edited_subjects)
        )
    else:
        message_text = COMPACT_USER_INFO.format(
            firstname=chat.first_name,
            lastname=f" {chat.last_name}" if chat.last_name is not None else "",
            username=f" @{chat.username}" if chat.username is not None else "",
            chat_id=message.chat.id,
            group_number=students[message.chat.id].group,
            notes_number=len(students[message.chat.id].notes),
            edited_classes_number=len(students[message.chat.id].edited_subjects)
        )
    
    await message.answer(text=message_text)
    
    students[message.chat.id].guard.text = Commands.SETTINGS.value
    students[message.chat.id].guard.drop()
