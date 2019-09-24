from bot import bot
from bot import students
from bot import metrics

from bot.commands.others.utilities.constants import FULL_USER_INFO
from bot.commands.others.utilities.constants import COMPACT_USER_INFO

from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.ME.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.ME)
def me(message):
    chat = bot.get_chat(chat_id=message.chat.id)
    
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
    
    bot.send_message(
        chat_id=message.chat.id,
        text=message_text
    )
