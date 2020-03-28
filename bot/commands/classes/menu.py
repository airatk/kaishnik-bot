from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.classes.utilities.keyboards import schedule_type

from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.CLASSES.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.CLASSES.value ]
)
@metrics.increment(Commands.CLASSES)
async def menu(message: Message):
    students[message.chat.id].guard.text = Commands.CLASSES.value
    
    request_entities: [str] = message.text.split()
    
    if len(request_entities) > 1:
        loading_message: Message = await message.answer(
            text=choice(LOADING_REPLIES),
            disable_web_page_preview=True
        )
        
        students[message.chat.id].another_group = request_entities[1]
        
        if students[message.chat.id].another_group_schedule_id is None:
            await loading_message.edit_text(
                text="Расписание занятий группы *{group}* получить не удалось :(".format(group=request_entities[1]),
                parse_mode="markdown"
            )
            
            students[message.chat.id].guard.drop()
            return
        
        await loading_message.delete()
    
    await message.answer(
        text="Тебе нужно расписание группы *{group}* на:".format(group=request_entities[1]) if len(request_entities) > 1 else "Тебе нужно расписание на:",
        parse_mode="markdown",
        reply_markup=schedule_type()
    )
