from bot import bot
from bot import students
from bot import metrics

from bot.commands.lecturers.utilities.keyboards import lecturer_chooser
from bot.commands.lecturers.utilities.keyboards import lecturer_info_type_chooser
from bot.commands.lecturers.utilities.constants import MAX_LECTURERS_NUMBER

from bot.shared.keyboards import cancel_option
from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ResponseError
from bot.shared.api.lecturers import get_lecturers_names
from bot.shared.commands import Commands

from random import choice


@bot.message_handler(
    commands=[ Commands.LECTURERS.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.LECTURERS)
def lecturers(message):
    guard_message = bot.send_message(
        chat_id=message.chat.id,
        text="Отправь фамилию или ФИО преподавателя.",
        reply_markup=cancel_option()
    )
    
    students[message.chat.id].guard.text = Commands.LECTURERS_NAME.value
    students[message.chat.id].guard.message = guard_message

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.LECTURERS_NAME.value)
def find_lecturer(message):
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text=choice(LOADING_REPLIES)
    )
    
    names = get_lecturers_names(name_part=message.text)
    
    if names is None:
        bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id].guard.drop()
        return
    elif names == []:
        bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text="Ничего не найдено :("
        )
        
        students[message.chat.id].guard.drop()
        return
    elif len(names) > MAX_LECTURERS_NUMBER:
        bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text="Слишком мало букв, слишком много преподавателей…"
        )
        
        students[message.chat.id].guard.drop()
        return
    
    bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text="Выбери преподавателя:",
        reply_markup=lecturer_chooser(names=names)
    )
    
    students[message.chat.id].guard.text = Commands.LECTURERS.value

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        Commands.LECTURERS.value in callback.data
)
@top_notification
def lecturers_schedule_type(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужны преподавателевы:",
        reply_markup=lecturer_info_type_chooser(lecturer_id=callback.data.split()[1])
    )
