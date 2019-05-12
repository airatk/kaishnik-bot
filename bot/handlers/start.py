from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.student import Student

from bot.keyboards.start import make_setup

from bot.helpers import save_to


@kbot.message_handler(func=lambda message: message.chat.id not in students)
@metrics.increment("start")
def start(message):
    students[message.chat.id] = Student()
    save_to(filename="data/users", object=students)
    
    students[message.chat.id].previous_message = "/start"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    kbot.send_message(
        chat_id=message.chat.id,
        text="Для начала настрой меня на общение с тобой😏",
        reply_markup=make_setup()
    )


@kbot.callback_query_handler(lambda callback: callback.message.chat.id not in students)
@top_notification
def unknown_user(callback): kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/start")
def gs_start(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
