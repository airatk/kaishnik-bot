from bot import kbot
from bot import students
from bot import metrics

from bot.student import Student

from bot.helpers import save_to


@kbot.message_handler(func=lambda message: message.chat.id not in students)
def start(message):
    metrics.increment("start")
    
    students[message.chat.id] = Student()
    
    students[message.chat.id].previous_message = "/start"  # Gate System (GS)
    
    save_to(filename="data/users", object=students)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "Для начала настрой меня на общение с тобой😏"
            "\n\n"
            "Отправь /settings"
        )
    )

@kbot.callback_query_handler(lambda callback: callback.message.chat.id not in students)
def unknown_user(callback): kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/start" and message.text != "/settings")
def gs_start(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
