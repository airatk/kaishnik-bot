from aiogram.types import Message

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
        await message.answer(text="Не доступно :(")
        await message.answer(text="Чтобы видеть номер зачётки и баллы, нужно перенастроиться с зачёткой, отправив /login")
        return
    
    await message.answer(
        text="Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(card=students[message.chat.id].card),
        parse_mode="markdown"
    )
