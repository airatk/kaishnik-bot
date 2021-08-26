from random import choice

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.login.menu import finish_login
from bot.platforms.vk.commands.login.utilities.keyboards import againer

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.keyboards import canceler

from bot.models.user import User

from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ResponseError
from bot.utilities.api.student import get_group_schedule_id
from bot.utilities.api.student import authenticate_user_via_kai_cas


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.LOGIN_BB.value }))
async def login_bb(event: SimpleBotEvent):
    User.update(
        group=None,
        group_schedule_id=None,
        bb_login=None,
        bb_password=None,
        is_setup=False
    ).where(
        User.vk_id == event.peer_id
    ).execute()
    
    await event.answer(
        message="Отправь логин от ББ.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Command.LOGIN_SET_BB_LOGIN.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Command.LOGIN_SET_BB_LOGIN.value
)
async def set_bb_login(event: SimpleBotEvent):
    User.update(
        bb_login=event.text
    ).where(
        User.vk_id == event.peer_id
    ).execute()
    
    await event.answer(
        message="Отправь пароль от ББ.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Command.LOGIN_SET_BB_PASSWORD.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Command.LOGIN_SET_BB_PASSWORD.value
)
async def set_bb_password(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )

    user: User = User.get(vk_id=event.peer_id)
    user.bb_password = event.text
    user.save()
    
    (_, response_error) = authenticate_user_via_kai_cas(user=user)

    if response_error is not None:
        if response_error is not ResponseError.INCORRECT_BB_CREDENTIALS:
            await event.answer(
                message=response_error.value,
                keyboard=to_menu()
            )

            guards[event.peer_id].drop()
            return
        
        await event.answer(
            message="\n\n".join([ response_error.value, "Отправь логин от ББ." ]),
            keyboard=canceler()
        )

        guards[event.peer_id].text = Command.LOGIN_SET_BB_LOGIN.value
        return

    await event.answer(
        message="Отправь номер своей группы.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Command.LOGIN_SET_GROUP.value


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.LOGIN_COMPACT.value }))
async def login_compact(event: SimpleBotEvent):
    User.update(
        group=None,
        group_schedule_id=None,
        bb_login=None,
        bb_password=None,
        is_setup=False
    ).where(
        User.vk_id == event.peer_id
    ).execute()
    
    await event.answer(
        message="Отправь номер своей группы.",
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Command.LOGIN_SET_GROUP.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Command.LOGIN_SET_GROUP.value
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
    
    User.update(
        group=event.text,
        group_schedule_id=group_schedule_id
    ).where(
        User.vk_id == event.peer_id
    ).execute()
    
    await finish_login(event=event)
