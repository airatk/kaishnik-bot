from typing import Any
from typing import Dict

from vkwave.bots import SimpleBotEvent
from vkwave.types.responses import UsersGetResponse
from vkwave.types.objects import UsersUserXtrCounters

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.settings.utilities.keyboards import action_chooser
from bot.platforms.vk.utilities.types import CommandsOfVK

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


@vk_bot.message_handler(
    lambda event:
        event.object.object.message.text.capitalize() == CommandsOfVK.SETTINGS.value
)
@increment_command_metrics(command=Commands.SETTINGS)
async def settings(event: SimpleBotEvent):
    vk_response: UsersGetResponse = await event.api_ctx.users.get(user_ids=[ event.peer_id ])
    vk_user: UsersUserXtrCounters = vk_response.response[0]
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    account_info: Dict[str, str] = {
        "fullname": " ".join([ vk_user.first_name, vk_user.last_name ]),
        "username": "" if vk_user.nickname is None else " @{username}".format(username=vk_user.nickname),
        "chat_id": event.peer_id,
        "notes_number": Notes.select().where(Notes.user_id == user_id).count()
    }
    message: str = ""
    
    user: Any = GroupsOfStudents.get_or_none(GroupsOfStudents.user_id == user_id)
    
    if user is None:
        user = CompactStudents.get_or_none(CompactStudents.user_id == user_id)
    if user is None:
        user = ExtendedStudents.get_or_none(ExtendedStudents.user_id == user_id)
    if user is None:
        user = BBStudents.get(BBStudents.user_id == user_id)
    
    if isinstance(user, GroupsOfStudents):
        account_info["group"] = user.group
        
        message = GROUP_OF_STUDENTS_INFO.format(**account_info)
    elif isinstance(user, CompactStudents):
        account_info["group"] = user.group
        
        message = COMPACT_STUDENT_INFO.format(**account_info)
    elif isinstance(user, ExtendedStudents):
        account_info["institute"] = user.institute[2:-2]
        account_info["year"] = user.year
        account_info["group"] = user.group
        account_info["name"] = user.name
        account_info["card"] = user.card
        
        message = EXTENDED_STUDENT_INFO.format(**account_info)
    elif isinstance(user, BBStudents):
        account_info["login"] = user.login
        
        message = BB_STUDENT_INFO.format(**account_info)
    
    await event.answer(
        message=message,
        keyboard=action_chooser()
    )
