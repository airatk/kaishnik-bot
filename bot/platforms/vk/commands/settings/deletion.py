from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.settings.utilities.keyboards import deletion_confirmer
from bot.platforms.vk.utilities.keyboards import make_start

from bot.models.user import User

from bot.utilities.types import Command


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.DELETE_ACCOUNT.value }))
async def deletion(event: SimpleBotEvent):
    await event.answer(
        message="Ты точно хочешь удалить свой аккаунт со всеми заметками и настройками?",
        keyboard=deletion_confirmer()
    )

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.DELETE_ACCOUNT_CONFIRM.value }))
async def deletion_confirm(event: SimpleBotEvent):
    User.delete().where(User.vk_id == event.peer_id).execute()
    
    await event.answer(
        message="Аккаунт удалён.",
        keyboard=make_start()
    )
