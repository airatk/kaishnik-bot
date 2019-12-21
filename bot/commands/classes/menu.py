from telebot.types import Message

from bot import bot
from bot import students
from bot import metrics

from bot.commands.classes.utilities.keyboards import schedule_type

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.commands import Commands

from random import choice


@bot.message_handler(
    commands=[ Commands.CLASSES.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.CLASSES)
def menu(message: Message):
    students[message.chat.id].guard.text = Commands.CLASSES.value
    
    request_entities: [str] = message.text.split()
    
    if len(request_entities) > 1:
        loading_message: Message = bot.send_message(
            chat_id=message.chat.id,
            text=choice(LOADING_REPLIES),
            disable_web_page_preview=True
        )
        
        students[message.chat.id].another_group = request_entities[1]
        
        if students[message.chat.id].another_group is None:
            bot.edit_message_text(
                chat_id=loading_message.chat.id,
                message_id=loading_message.message_id,
                text="Расписание занятий для группы *{group}* получить не удалось :(".format(group=request_entities[1]),
                parse_mode="Markdown"
            )
            
            students[message.chat.id].guard.drop()
            return
        else:
            bot.delete_message(chat_id=loading_message.chat.id, message_id=loading_message.message_id)
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Тебе нужно расписание на:",
        reply_markup=schedule_type()
    )
