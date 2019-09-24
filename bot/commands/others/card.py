from bot import bot
from bot import students
from bot import metrics

from bot.shared.commands import Commands


@bot.message_handler(
    commands=[ Commands.CARD.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.CARD)
def card(message):
    if not students[message.chat.id].is_full:
        bot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Чтобы видеть номер зачётки и баллы, нужно перенастроиться с зачёткой, отправив /login"
        )
        return
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(card=students[message.chat.id].card),
        parse_mode="Markdown"
    )
