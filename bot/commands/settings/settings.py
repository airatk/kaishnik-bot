from aiogram.types import Chat
from aiogram.types import Message

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.settings.utilities.keyboards import action_chooser
from bot.commands.settings.utilities.constants import FULL_USER_INFO
from bot.commands.settings.utilities.constants import COMPACT_USER_INFO

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.SETTINGS.value ]
)
@metrics.increment(Commands.SETTINGS)
async def settings(message: Message):
    chat: Chat = await message.bot.get_chat(chat_id=message.chat.id)
    
    info: {str: str} = {
        "firstname": chat.first_name,
        "lastname": " {lastname}".format(lastname=chat.last_name) if chat.last_name is not None else "",
        "username": " @{username}".format(username=chat.username) if chat.username is not None else "",
        "chat_id": message.chat.id,
        "group": students[message.chat.id].group,
        "notes_number": len(students[message.chat.id].notes),
        "edited_classes_number": len(students[message.chat.id].edited_subjects)
    }
    
    message_text: str = FULL_USER_INFO.format(
        **info,
        institute=students[message.chat.id].institute,
        year=students[message.chat.id].year,
        name=students[message.chat.id].name,
        card=students[message.chat.id].card
    ) if students[message.chat.id].is_full else COMPACT_USER_INFO.format(**info)
    
    # Removing emojies
    message_text = message_text.replace("\u2665 ", "").replace(" \u2665", "")
    
    await message.answer(
        text=message_text,
        reply_markup=action_chooser()
    )
    
    students[message.chat.id].guard.text = Commands.SETTINGS.value
