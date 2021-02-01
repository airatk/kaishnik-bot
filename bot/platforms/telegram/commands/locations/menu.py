from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.locations.utilities.keyboards import location_type_chooser

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.LOCATIONS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.LOCATIONS.value ]
)
@increment_command_metrics(command=Commands.LOCATIONS)
async def locations(message: Message):
    await message.answer(
        text="Аж 4 варианта на выбор:",
        reply_markup=location_type_chooser()
    )
    
    guards[message.chat.id].text = Commands.LOCATIONS.value
