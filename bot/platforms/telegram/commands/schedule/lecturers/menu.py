from typing import Dict
from typing import List

from random import choice

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.schedule.lecturers.utilities.keyboards import lecturer_chooser
from bot.platforms.telegram.commands.schedule.lecturers.utilities.keyboards import lecturer_info_type_chooser
from bot.platforms.telegram.commands.schedule.lecturers.utilities.constants import MAX_LECTURERS_NUMBER

from bot.platforms.telegram.utilities.keyboards import canceler
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.lecturers import get_lecturers_names


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.LECTURERS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.LECTURERS.value ]
)
@increment_command_metrics(command=Commands.LECTURERS)
async def lecturers(message: Message):
    guard_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (lecturers_names, response_error) = get_lecturers_names()
    
    if lecturers_names is None:
        await guard_message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        return
    
    states[message.chat.id].lecturers_names = lecturers_names
    
    await guard_message.edit_text(
        text="Отправь фамилию или ФИО преподавателя.",
        reply_markup=canceler()
    )
    
    guards[message.chat.id].text = Commands.LECTURERS_NAME.value
    guards[message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and guards[message.chat.id].text == Commands.LECTURERS_NAME.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Commands.LECTURERS_NAME.value
)
async def find_lecturer(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    
    partial_name_parts: List[str] = message.text.lower().split(" ")
    names: List[Dict[str, str]] = list(filter(
        lambda name: all(partial_name_part in name["lecturer"].lower() for partial_name_part in partial_name_parts),
        states[message.chat.id].lecturers_names
    ))
    
    if len(names) == 0:
        await guards[message.chat.id].message.edit_text(
            text=(
                "Ничего не найдено :(\n\n"
                "Попробуешь ещё раз?"
            ),
            reply_markup=canceler()
        )
        return
    
    if len(names) > MAX_LECTURERS_NUMBER:
        await guards[message.chat.id].message.edit_text(
            text=(
                "Слишком мало букв, слишком много преподавателей…\n\n"
                "Попробуешь ещё раз?"
            ),
            reply_markup=canceler()
        )
        return
    
    await guards[message.chat.id].message.edit_text(
        text="Выбери преподавателя:",
        reply_markup=lecturer_chooser(names=names)
    )
    
    guards[message.chat.id].text = Commands.LECTURERS.value

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LECTURERS.value and
        Commands.LECTURERS.value in callback.data
)
@top_notification
async def lecturers_schedule_type(callback: CallbackQuery):
    lecturer_id: str = callback.data.split()[1]
    
    names: List[str] = list(filter(
        lambda lecturer: lecturer["id"] == lecturer_id,
        states[callback.message.chat.id].lecturers_names
    ))
    chosen_name: str = "".join([ "*", names[0]["lecturer"].replace(" ", "\n", 1), "*" ])
    
    await callback.message.edit_text(
        text=chosen_name,
        parse_mode=ParseMode.MARKDOWN
    )
    
    await callback.message.answer(
        text="Тебе нужны преподавателевы:",
        reply_markup=lecturer_info_type_chooser(lecturer_id=lecturer_id)
    )
