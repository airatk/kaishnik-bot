from random import choice

from re import Match

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.login.menu import finish_login
from bot.platforms.vk.commands.login.utilities.keyboards import againer

from bot.platforms.vk.utilities.keyboards import canceler

from bot.models.users import Users
from bot.models.compact_students import CompactStudents
from bot.models.bb_students import BBStudents

from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ResponseError
from bot.utilities.api.student import get_group_schedule_id


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_COMPACT.value }))
async def login_compact(event: SimpleBotEvent):
    user: Users = Users.get(vk_id=event.peer_id)
    
    CompactStudents.delete().where(CompactStudents.user_id == user.user_id).execute()
    BBStudents.delete().where(BBStudents.user_id == user.user_id).execute()
    
    user.is_setup = False
    user.save()
    
    CompactStudents.create(user_id=user.user_id).save()
    
    await event.answer(
        message="Отправь номер своей группы.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Commands.LOGIN_COMPACT.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Commands.LOGIN_COMPACT.value
)
async def set_group(event: SimpleBotEvent):
    guards[event.peer_id].drop()

    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    (group_schedule_id, response_error) = get_group_schedule_id(group=event.text)
    
    if group_schedule_id is None:
        if response_error is ResponseError.NO_RESPONSE:
            (message, keyboard) = (response_error.value, None)
        else:
            (message, keyboard) = ("\n\n".join([ response_error.value, "Попробуй снова?" ]), againer())
        
        await event.answer(
            message=message, 
            keyboard=keyboard
        )
        
        return
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    
    CompactStudents.update(
        group=event.text,
        group_schedule_id=group_schedule_id
    ).where(
        CompactStudents.user_id == user_id
    ).execute()
    
    await finish_login(event=event)
