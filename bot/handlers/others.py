from bot import kbot
from bot import students
from bot import metrics

from bot.constants import BRS
from bot.constants import HELP
from bot.constants import DONATE

from bot.keyboards.settings import set_card_skipper

from bot.helpers import is_even


@kbot.message_handler(
    commands=["week"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("week")
def week(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text="Текущая неделя {type}.".format(type="чётная" if is_even() else "нечётная")
    )


@kbot.message_handler(
    commands=["card"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("card")
def card(message):
    if students[message.chat.id].student_card_number == "unset":
        students[message.chat.id].previous_message = "/card"  # Gate System (GS)
        
        kbot.send_message(
            chat_id=message.chat.id,
            text=(
                "Отправь номер своей зачётки "
                "(интересный факт — студенческий билет и зачётка имеют одинаковый номер!)."
                "\n\n"
                "Либо пропусти, но баллы показать не смогу."
            ),
            reply_markup=set_card_skipper()
        )
    elif students[message.chat.id].institute_id == "КИТ":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(
                card=students[message.chat.id].student_card_number
            ),
            parse_mode="Markdown"
        )


@kbot.message_handler(
    commands=["brs"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("brs")
def brs(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=BRS,
        parse_mode="Markdown"
    )


@kbot.message_handler(
    commands=["help"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("help")
def help(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=HELP,
        parse_mode="Markdown"
    )


@kbot.message_handler(
    commands=["donate"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("donate")
def donate(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=DONATE,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
