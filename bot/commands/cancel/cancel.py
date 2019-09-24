from bot import bot
from bot import students
from bot import metrics

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.CANCEL.value ],
    func=lambda message: message.chat.id in students
)
@metrics.increment(Commands.CANCEL)
def cancel_on_command(message):
    if students[message.chat.id].guard.text is None:
        bot.send_message(
            chat_id=message.chat.id,
            text="Запущенных команд нет. Отправь какую-нибудь☺️"
        )
        return
    
    students[message.chat.id].guard.drop()
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Отменено!"
    )

@bot.callback_query_handler(
    func=lambda callback:
        callback.message.chat.id in students and
        callback.data == Commands.CANCEL.value
)
@top_notification
def cancel_on_callback(callback):
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    cancel_on_command(callback.message)
