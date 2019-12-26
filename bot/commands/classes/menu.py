from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.classes.utilities.keyboards import schedule_type

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.CLASSES.value ]
)
@metrics.increment(Commands.CLASSES)
async def menu(message: Message):
    students[message.chat.id].guard.text = Commands.CLASSES.value
    
    request_entities: [str] = message.text.split()
    
    if len(request_entities) > 1:
        loading_message: Message = await bot.send_message(
            chat_id=message.chat.id,
            text=choice(LOADING_REPLIES),
            disable_web_page_preview=True
        )
        
        students[message.chat.id].another_group = request_entities[1]
        
        if students[message.chat.id].another_group is None:
            await bot.edit_message_text(
                chat_id=loading_message.chat.id,
                message_id=loading_message.message_id,
                text="Расписание занятий группы *{group}* получить не удалось :(".format(group=request_entities[1])
            )
            
            students[message.chat.id].guard.drop()
            return
        else:
            await bot.delete_message(chat_id=loading_message.chat.id, message_id=loading_message.message_id)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Тебе нужно расписание{group} на:".format(group=" группы " + request_entities[1]),
        reply_markup=schedule_type()
    )
