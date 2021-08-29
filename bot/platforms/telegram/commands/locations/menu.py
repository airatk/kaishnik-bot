from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.locations.utilities.keyboards import location_type_chooser

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.LOCATIONS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.LOCATIONS.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.LOCATIONS)
async def locations(message: Message):
    await message.answer(
        text="Аж 4 варианта на выбор:",
        reply_markup=location_type_chooser()
    )
    
    guards[message.chat.id].text = Command.LOCATIONS.value
