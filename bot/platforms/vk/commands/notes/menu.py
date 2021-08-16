from peewee import ModelSelect

from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.notes.utilities.keyboards import action_chooser
from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.models.users import Users
from bot.models.notes import Notes

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text == CommandsOfVK.NOTES.value
)
@increment_command_metrics(command=Commands.NOTES)
async def notes(event: SimpleBotEvent):
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    user_notes: ModelSelect = Notes.select().where(Notes.user_id == user_id)
    
    await event.answer(
        message="Заметок всего: {current}/{max}".format(
            current=user_notes.count(),
            max=MAX_NOTES_NUMBER
        ),
        keyboard=action_chooser(has_notes=user_notes.exists())
    )
