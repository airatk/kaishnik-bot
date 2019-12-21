from telebot.types import Message

from bot import bot
from bot import students
from bot import metrics

from bot.commands.edit.utilities.keyboards import action_chooser

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.EDIT.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.EDIT)
def edit(message: Message):
    edited_number: int = len(students[message.chat.id].edited_subjects)
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Отредактировано пар: *{edited_number}*".format(edited_number=edited_number),
        reply_markup=action_chooser(has_edits=edited_number != 0),
        parse_mode="Markdown"
    )
    
    students[message.chat.id].guard.text = Commands.EDIT.value
