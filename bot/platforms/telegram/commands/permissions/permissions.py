from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatMember

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.commands.permissions.utilities.helpers import get_bot_member
from bot.platforms.telegram.commands.permissions.utilities.helpers import check_permissions_in_group_chat_on_command
from bot.platforms.telegram.commands.permissions.utilities.helpers import check_permissions_in_group_chat_on_callback

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command


@dispatcher.message_handler(
    check_permissions_in_group_chat_on_command,
    content_types=[ "text" ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.NO_PERMISSIONS)
async def permissions_on_command(message: Message):
    bot_member: ChatMember = await get_bot_member(message=message)
    
    text: str = ""
    
    if not bot_member.is_chat_admin():
        text = "".join([ text, "быть админом" ])
    if not bot_member.can_delete_messages:
        text = ("" if text == "" else " и ").join([ text, "иметь право удалять сообщения" ])
    
    await message.answer(text="".join([
        "Бот должен ", text, ".\n",
        "Это можно изменить в настройках чата.",
    ]))

@dispatcher.callback_query_handler(check_permissions_in_group_chat_on_callback)
@top_notification
async def permissions_on_callback(callback: CallbackQuery):
    await permissions_on_command(callback.message)
