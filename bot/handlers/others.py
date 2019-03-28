from bot import kaishnik
from bot import students
from bot import metrics

from bot.constants import BRS

from bot.keyboards.others import remove_keyboard
from bot.keyboards.others import skipper

@kaishnik.message_handler(commands=["card"])
def card(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("card")
    
    if students[message.chat.id].student_card_number == "unset":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Номер зачётки не указан, поэтому отправь его "
                 "(интересный факт — номер твоего студенческого и номер твоей зачётки одинаковы!).",
            reply_markup=remove_keyboard()
        )
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
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
            text=students[message.chat.id].get_card(),
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
