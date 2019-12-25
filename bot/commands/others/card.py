from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.CARD.value ]
)
@metrics.increment(Commands.CARD)
async def card(message: Message):
    if not students[message.chat.id].is_full:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Чтобы видеть номер зачётки и баллы, нужно перенастроиться с зачёткой, отправив /login"
        )
        return
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(card=students[message.chat.id].card)
    )
