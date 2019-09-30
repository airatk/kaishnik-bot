from bot import bot
from bot import students
from bot import metrics

from bot.commands.login.utilities.keyboards import login_way_chooser

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.LOGIN.value ],
    func=lambda message:
        students[message.chat.id].guard.text == Commands.START.value or
        students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.LOGIN)
def login_on_command(message):
    guard_message = bot.send_message(
        chat_id=message.chat.id,
        text=(
            "{warning}"
            "Студенческий билет и зачётка имеют одинаковый номер😉\n\n"
            "Выбери желаемый путь настройки:"
        ).format(
            # Showing the warning to the old users
            warning="Все текущие данные, включая *заметки* и *изменённое расписание*, будут стёрты.\n\n" if students[message.chat.id].is_setup else ""
        ),
        reply_markup=login_way_chooser(is_old=students[message.chat.id].is_setup),
        parse_mode="Markdown"
    )
    
    students[message.chat.id].guard.text = Commands.LOGIN.value

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.START.value and
        callback.data == Commands.LOGIN.value
)
@metrics.increment(Commands.LOGIN)
@top_notification
def login_on_callback(callback):
    # Cleanning the chat
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    bot.delete_message(chat_id=callback.message.chat.id, message_id=students[callback.message.chat.id].guard.message.message_id)
    
    login_on_command(callback.message)
