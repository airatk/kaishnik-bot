from typing import Any
from typing import Dict

from aiogram.types import Message
from aiogram.types import Chat
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.settings.utilities.keyboards import action_chooser

from bot.models.users import Users
from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents
from bot.models.notes import Notes

from bot.utilities.constants import GROUP_OF_STUDENTS_INFO
from bot.utilities.constants import COMPACT_STUDENT_INFO
from bot.utilities.constants import EXTENDED_STUDENT_INFO
from bot.utilities.constants import BB_STUDENT_INFO
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.SETTINGS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.SETTINGS.value ]
)
@increment_command_metrics(command=Commands.SETTINGS)
async def settings(message: Message):
    chat: Chat = await message.bot.get_chat(chat_id=message.chat.id)
    
    user_id: int = Users.get(Users.telegram_id == message.chat.id).user_id
    account_info: Dict[str, str] = {
        "fullname": chat.full_name,
        "username": "" if chat.username is None else " @{username}".format(username=chat.username),
        "chat_id": message.chat.id if message.chat.type == ChatType.PRIVATE else -(message.chat.id + 1_000_000_000_000),
        "notes_number": Notes.select().where(Notes.user_id == user_id).count()
    }
    text: str = ""
    
    user: Any = GroupsOfStudents.get_or_none(GroupsOfStudents.user_id == user_id)
    
    if user is None:
        user = CompactStudents.get_or_none(CompactStudents.user_id == user_id)
    if user is None:
        user = ExtendedStudents.get_or_none(ExtendedStudents.user_id == user_id)
    if user is None:
        user = BBStudents.get(BBStudents.user_id == user_id)
    
    if isinstance(user, GroupsOfStudents):
        account_info["group"] = user.group
        
        text = GROUP_OF_STUDENTS_INFO.format(**account_info)
    elif isinstance(user, CompactStudents):
        account_info["group"] = user.group
        
        text = COMPACT_STUDENT_INFO.format(**account_info)
    elif isinstance(user, ExtendedStudents):
        account_info["institute"] = user.institute[2:-2]
        account_info["year"] = user.year
        account_info["group"] = user.group
        account_info["name"] = user.name
        account_info["card"] = user.card
        
        text = EXTENDED_STUDENT_INFO.format(**account_info)
    elif isinstance(user, BBStudents):
        account_info["login"] = user.login
        
        text = BB_STUDENT_INFO.format(**account_info)
    
    await message.answer(
        text=text,
        reply_markup=action_chooser()
    )
    
    guards[message.chat.id].text = Commands.SETTINGS.value
