from bot import bot
from bot import students
from bot import metrics

from bot.commands.start.utilities.keyboards import make_login

from bot.shared.helpers import top_notification
from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


# Accepting old users on `/start` command whole new users on any messsage...
@bot.message_handler(
    func=lambda message:
        message.text == "/" + Commands.START.value or
        message.chat.id not in students
)
@metrics.increment(Commands.START)
def start_on_command(message):
    students[message.chat.id] = Student()
    save_data(file=USERS_FILE, object=students)
    
    guard_message = bot.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Для начала настрой меня на общение с тобой😏",
        reply_markup=make_login()
    )
    
    students[message.chat.id].guard.text = Commands.START.value
    students[message.chat.id].guard.message = guard_message

# ... & any callback
@bot.callback_query_handler(lambda callback: callback.message.chat.id not in students)
@metrics.increment(Commands.START)
@top_notification
def start_on_callback(callback):
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    start_on_command(callback.message)
