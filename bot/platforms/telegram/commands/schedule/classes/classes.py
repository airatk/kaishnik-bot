from random import choice

from typing import List

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.schedule.utilities.keyboards import time_period_chooser
from bot.platforms.telegram.commands.schedule.utilities.classes import common_add_chosen_date
from bot.platforms.telegram.commands.schedule.utilities.classes import common_show_chosen_dates

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.student import get_group_schedule_id


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.CLASSES.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.CLASSES.value ]
)
@increment_command_metrics(command=Commands.CLASSES)
async def menu(message: Message):
    loading_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    classes_arguments: List[str] = message.text.split()[1:]
    
    if len(classes_arguments) != 0:
        (another_group_schedule_id, response_error) = get_group_schedule_id(group=classes_arguments[0])
        
        if another_group_schedule_id is None:
            await loading_message.edit_text(
                text="\n".join([
                    "Расписание занятий группы *{group}* получить не удалось.".format(group=classes_arguments[0]),
                    response_error.value
                ]),
                parse_mode="markdown"
            )
            return
        
        states[message.chat.id].another_group_schedule_id = another_group_schedule_id
    
    await loading_message.edit_text(
        text="Тебе нужно расписание{for_another_group} на:".format(
            for_another_group=" группы *{group}*".format(group=classes_arguments[0]) if len(classes_arguments) != 0 else ""
        ),
        parse_mode="markdown",
        reply_markup=time_period_chooser()
    )
    
    states[message.chat.id].chosen_schedule_dates = []
    guards[message.chat.id].text = Commands.CLASSES.value

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.CLASSES.value and
        Commands.CLASSES_CHOOSE.value in callback.data
)
@top_notification
async def add_chosen_date(callback: CallbackQuery):
    await common_add_chosen_date(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.CLASSES.value and
        Commands.CLASSES_SHOW.value in callback.data
)
@top_notification
async def show_chosen_dates(callback: CallbackQuery):
    await common_show_chosen_dates(command=Commands.CLASSES, callback=callback)
