from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.keyboards import canceler

from bot.models.user import User
from bot.models.note import Note

from bot.utilities.helpers import clarify_markdown
from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.types import Command


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.NOTES_ADD.value }))
async def add_note_hint(event: SimpleBotEvent):
    user: User = User.get(User.vk_id == event.peer_id)
    note_number: int = Note.select().where(Note.user == user).count() + 1
    
    if note_number > MAX_NOTES_NUMBER:
        await event.answer(
            message="{max}-заметковый лимит уже достигнут.".format(max=MAX_NOTES_NUMBER),
            keyboard=to_menu()
        )
        return
    
    await event.answer(
        message=(
            f"Добавляемая заметка будет {note_number} по счёту.\n"
            "\n"
            "• Используй звёздочки, чтобы выделить *жирным*\n"
            "• Используй нижнее подчёркивание, чтобы выделить _курсивом_\n"
            "• Жирный и курсив будут отображаться только в Телеграме.\n"
            "\n"
            "Напиши заметку и отправь решительно."
        ),
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Command.NOTES_ADD.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Command.NOTES_ADD.value
)
async def add_note(event: SimpleBotEvent):
    Note.insert(
        user=User.get(User.vk_id == event.peer_id),
        text=clarify_markdown(event.text)
    ).execute()
    
    await event.answer(
        message="Запомнено!",
        keyboard=to_menu()
    )
    
    guards[event.peer_id].drop()
