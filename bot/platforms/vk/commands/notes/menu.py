from peewee import ModelSelect

from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.notes.utilities.keyboards import action_chooser
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize() == CommandOfVK.NOTES.value
)
@note_metrics(platform=Platform.VK, command=Command.NOTES)
async def notes(event: SimpleBotEvent):
    user: User = User.get(User.vk_id == event.peer_id)
    user_notes: ModelSelect = Note.select().where(Note.user == user)
    
    await event.answer(
        message="Заметок всего: {current}/{max}".format(
            current=len(user_notes),
            max=MAX_NOTES_NUMBER
        ),
        keyboard=action_chooser(has_notes=user_notes.exists())
    )
