from bot import kaishnik
from bot import students
from bot import metrics

from bot.constants import BRS
from bot.constants import DONATE

from bot.keyboards.others import skipper

from telebot.types import ReplyKeyboardRemove

@kaishnik.message_handler(commands=["card"])
def card(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("card")
    
    if students[message.chat.id].student_card_number == "unset":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text=(
                "Номер зачётки не указан, поэтому отправь его "
                "(интересный факт — студенческий билет и зачётка имеют одинаковый номер!)."
            ),
            reply_markup=ReplyKeyboardRemove()
        )
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Либо пропусти, но баллы показать не смогу.",
            reply_markup=skipper(
                text="пропустить",
                callback_data="skip"
            )
        )
    elif students[message.chat.id].institute_id == "КИТ":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(
                card=students[message.chat.id].student_card_number
            ),
            parse_mode="Markdown"
        )

@kaishnik.message_handler(commands=["brs"])
def brs(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("brs")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=BRS,
        parse_mode="Markdown"
    )

@kaishnik.message_handler(commands=["donate"])
def donate(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("donate")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=DONATE,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
