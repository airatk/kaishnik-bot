from bot import kbot
from bot import students


@kbot.message_handler(commands=[ "cancel" ])
def cancel(message):
    if students[message.chat.id].previous_message is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Запущенных команд нет. Отправь какую-нибудь☺️"
        )
        return
    
    students[message.chat.id].previous_message = None  # Gates System (GS)

    kbot.send_message(
        chat_id=message.chat.id,
        text="Отменено!"
    )


# (all the commands & other stuff handlers) - 1
from bot.handlers import creator

from bot.handlers import start
from bot.handlers import settings

from bot.handlers import classes
from bot.handlers import exams
from bot.handlers import lecturers
from bot.handlers import score

from bot.handlers import notes
from bot.handlers import edit

from bot.handlers import locations
from bot.handlers import others

from bot.handlers import unknown
