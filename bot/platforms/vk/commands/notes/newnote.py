from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.keyboards import canceler

from bot.models.users import Users
from bot.models.notes import Notes

from bot.utilities.helpers import clarify_markdown
from bot.utilities.constants import MAX_NOTES_NUMBER
from bot.utilities.types import Commands


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.NOTES_ADD.value }))
async def add_note_hint(event: SimpleBotEvent):
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    note_number: int = Notes.select().where(Notes.user_id == user_id).count() + 1
    
    if note_number > MAX_NOTES_NUMBER:
        await event.answer(text="{max}-заметковый лимит уже достигнут.".format(max=MAX_NOTES_NUMBER))
        return
    
    await event.answer(
        message=(
            "Добавляемая заметка будет {note_number} по счёту.\n\n"
            "• Используй звёздочки, чтобы выделить *жирным*\n"
            "• Используй нижнее подчёркивание, чтобы выделить _курсивом_\n"
            "• Жирный и курсив будут отображаться только в Телеграме.\n\n"
            "Напиши заметку и отправь решительно.".format(note_number=note_number)
        ),
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Commands.NOTES_ADD.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Commands.NOTES_ADD.value
)
async def add_note(event: SimpleBotEvent):
    Notes.create(
        user_id=Users.get(Users.vk_id == event.peer_id).user_id,
        note=clarify_markdown(event.text)
    )
    
    await event.answer(
        message="Запомнено!",
        keyboard=to_menu()
    )
    
    guards[event.peer_id].drop()
