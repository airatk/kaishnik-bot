from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.locations.utilities.keyboards import location_type_chooser

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.LOCATIONS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text is None,
    commands=[ Commands.LOCATIONS.value ]
)
@metrics.increment(Commands.LOCATIONS)
async def locations(message: Message):
    await message.answer(
        text="Аж 4 варианта на выбор:",
        reply_markup=location_type_chooser()
    )
    
    students[message.chat.id].guard.text = Commands.LOCATIONS.value