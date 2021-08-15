from random import choice

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards
from bot.platforms.vk import states

from bot.platforms.vk.commands.login.menu import finish_login
from bot.platforms.vk.commands.login.utilities.keyboards import institute_setter
from bot.platforms.vk.commands.login.utilities.keyboards import year_setter
from bot.platforms.vk.commands.login.utilities.keyboards import group_setter
from bot.platforms.vk.commands.login.utilities.keyboards import name_setter

from bot.platforms.vk.utilities.keyboards import canceler

from bot.models.users import Users
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents

from bot.utilities.types import Commands
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.constants import INSTITUTES
from bot.utilities.api.types import ExtendedLoginDataType
from bot.utilities.api.types import ResponseError
from bot.utilities.api.student import get_group_schedule_id
from bot.utilities.api.student import get_extended_login_data
from bot.utilities.api.student import get_last_available_semester


# PATCH: Temporary patch necessary because of unavailablity of old.kai.ru
from bot.platforms.vk.commands.login.utilities.keyboards import againer

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_EXTENDED.value }))
async def temporary_extended_login_handler(event: SimpleBotEvent):
    await event.answer(
        message="К сожалению, часть функционала отвалилась со стороны серверов kai.ru, поэтому этот вариант входа временно недоступен.",
        dont_parse_links=True,
        keyboard=againer()
    )
# ENDPATCH


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_EXTENDED.value }))
async def login_extended(event: SimpleBotEvent):
    user: Users = Users.get(vk_id=event.peer_id)
    
    CompactStudents.delete().where(CompactStudents.user_id == user.user_id).execute()
    ExtendedStudents.delete().where(ExtendedStudents.user_id == user.user_id).execute()
    BBStudents.delete().where(BBStudents.user_id == user.user_id).execute()
    
    user.is_setup = False
    user.save()
        
    ExtendedStudents.create(user_id=user.user_id).save()
    
    await event.answer(
        message="Выбери институт (привет, ФМФ🌚).",
        keyboard=institute_setter()
    )

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_SET_INSTITUTE.value }))
async def set_institute(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    # Setting institute
    institute_id: str = event.payload["institute_id"]
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    
    ExtendedStudents.update(
        institute=INSTITUTES[institute_id],
        institute_id=institute_id
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    # Asking for year
    (years, response_error) = get_extended_login_data(extended_login_data_type=ExtendedLoginDataType.YEARS, user_id=user_id)
    
    if years is None:
        await event.answer(
            message=response_error.value,
            dont_parse_links=True
        )
        return
    
    await event.answer(
        message="Выбери курс.",
        keyboard=year_setter(years)
    )

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_SET_YEAR.value }))
async def set_year(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    # Setting year
    year: str = event.payload["year"]

    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    
    ExtendedStudents.update(
        year=year
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    # Asking for group
    (groups, response_error) = get_extended_login_data(extended_login_data_type=ExtendedLoginDataType.GROUPS, user_id=user_id)
    
    if groups is None:
        await event.answer(
            message=response_error.value,
            dont_parse_links=True
        )
        return
    
    states[event.peer_id].groups = groups

    await event.answer(
        message="Выбери номер группы.",
        keyboard=group_setter(groups=groups)
    )


@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_SET_GROUP.value }))
async def set_group(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    # Setting group
    group: str = event.payload["group"]
    group_id: str = event.payload["group_id"]
    
    (group_schedule_id, response_error) = get_group_schedule_id(group=group)
    
    if group_schedule_id is None:
        await event.answer(
            text=response_error.value,
            disable_web_page_preview=True
        )
        return
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    
    ExtendedStudents.update(
        group=group_id,
        group_schedule_id=group_schedule_id,
        group_score_id=group_id
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    # Asking for name
    (group_names, response_error) = get_extended_login_data(extended_login_data_type=ExtendedLoginDataType.NAMES, user_id=user_id)
    
    if group_names is None:
        await event.answer(
            message=response_error.value,
            dont_parse_links=True
        )
        return
    
    states[event.peer_id].group_names = { name_id: name for (name, name_id) in group_names }
    
    await event.answer(
        message="Выбери себя.",
        keyboard=name_setter(names=list(states[event.peer_id].group_names.items()))
    )

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Commands.LOGIN_SET_NAME.value }))
async def set_name(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    # Setting name
    name_id: str = event.payload["name_id"]
    
    ExtendedStudents.update(
        name=states[event.peer_id].group_names[name_id],
        name_id=name_id
    ).where(
        ExtendedStudents.user_id == Users.get(Users.vk_id == event.peer_id).user_id
    ).execute()
    
    # Asking for student card number
    await event.answer(
        message=(
            "Отправь номер студенческого или зачётки.\n\n"
            "Если ты платник, нужно добавить большую букву \"П\" перед ним."
        ),
        keyboard=canceler()
    )
    
    guards[event.peer_id].text = Commands.LOGIN_SET_CARD.value

@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text == Commands.LOGIN_SET_CARD.value
)
async def set_card(event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    user_id: int = Users.get(Users.vk_id == event.peer_id).user_id
    
    ExtendedStudents.update(
        card=event.text
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    (last_available_semester, response_error) = get_last_available_semester(user_id=user_id, is_card_check=True)
    
    if last_available_semester is None:
        await event.answer(
            message=response_error.value,
            keyboard=canceler() if response_error is ResponseError.INCORRECT_CARD else None,
            dont_parse_links=True
        )
        
        if response_error is not ResponseError.INCORRECT_CARD:
            guards[event.peer_id].drop()
        
        return
    
    await finish_login(event=event)
