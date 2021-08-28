from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ChatMember


async def get_bot_member(message: Message) -> ChatMember:
    bot_user = await message.bot.me
    bot_member = await message.chat.get_member(user_id=bot_user.id)
    
    return bot_member


async def check_permissions_in_group_chat_on_command(message: Message) -> bool:
    if message.chat.type == ChatType.PRIVATE: return False
    if not (message.is_command() or message.reply_to_message is not None and message.reply_to_message.from_user.is_bot): return False
    
    bot_member = await get_bot_member(message=message)
    
    return not (bot_member.is_chat_admin() and bot_member.can_delete_messages)

async def check_permissions_in_group_chat_on_callback(callback: CallbackQuery) -> bool:
    return await check_permissions_in_group_chat_on_command(message=callback.message)
