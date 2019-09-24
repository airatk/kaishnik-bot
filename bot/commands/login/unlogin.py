from bot import bot
from bot import students
from bot import metrics

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@bot.message_handler(func=lambda message: not students[message.chat.id].is_setup)
@metrics.increment(Commands.UNLOGIN)
def deny_access_on_message(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Первоначальная настройка пройдена не полностью, исправляйся — /login"
    )
    
    students[message.chat.id].guard.drop()

@bot.callback_query_handler(func=lambda callback: not students[callback.message.chat.id].is_setup)
@top_notification
def deny_access_on_callback(callback):
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    deny_access_on_message(callback.message)
