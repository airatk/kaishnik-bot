from random import choice

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.login.menu import finish_login
from bot.platforms.telegram.commands.login.utilities.keyboards import institute_setter
from bot.platforms.telegram.commands.login.utilities.keyboards import year_setter
from bot.platforms.telegram.commands.login.utilities.keyboards import group_setter
from bot.platforms.telegram.commands.login.utilities.keyboards import name_setter

from bot.platforms.telegram.utilities.keyboards import canceler
from bot.platforms.telegram.utilities.helpers import top_notification

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


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN.value and
        callback.data == Commands.LOGIN_EXTENDED.value
)
@top_notification
async def login_extended(callback: CallbackQuery):
    user: Users = Users.get(telegram_id=callback.message.chat.id)
    
    CompactStudents.delete().where(CompactStudents.user_id == user.user_id).execute()
    ExtendedStudents.delete().where(ExtendedStudents.user_id == user.user_id).execute()
    BBStudents.delete().where(BBStudents.user_id == user.user_id).execute()
    
    user.is_setup = False
    user.save()
        
    ExtendedStudents.create(user_id=user.user_id).save()
    
    await callback.message.edit_text(
        text="Выбери институт (привет, ФМФ🌚):",
        reply_markup=institute_setter()
    )
    
    guards[callback.message.chat.id].text = Commands.LOGIN_EXTENDED.value

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_INSTITUTE.value in callback.data
)
@top_notification
async def set_institute(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        parse_mode="markdown",
        disable_web_page_preview=True
    )
    
    # Setting institute
    institute_id: str = callback.data.split()[1]
    
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    
    ExtendedStudents.update(
        institute=INSTITUTES[institute_id],
        institute_id=institute_id
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    # Asking for year
    (years, response_error) = get_extended_login_data(extended_login_data_type=ExtendedLoginDataType.YEARS, user_id=user_id)
    
    if years is None:
        await callback.message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        
        guards[callback.message.chat.id].drop()
        return
    
    await callback.message.edit_text(
        text="Выбери курс:",
        reply_markup=year_setter(years)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_YEAR.value in callback.data
)
@top_notification
async def set_year(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting year
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    
    ExtendedStudents.update(
        year=callback.data.split()[1]
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    # Asking for group
    (groups, response_error) = get_extended_login_data(extended_login_data_type=ExtendedLoginDataType.GROUPS, user_id=user_id)
    
    if groups is None:
        await callback.message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        
        guards[callback.message.chat.id].drop()
        return
    
    states[callback.message.chat.id].groups = groups

    await callback.message.edit_text(
        text="Выбери номер группы:",
        reply_markup=group_setter(groups=groups)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN_EXTENDED.value and (
            callback.data.startswith(Commands.LOGIN_GROUPS_NEXT_PAGE.value) or
            callback.data.startswith(Commands.LOGIN_GROUPS_PREVIOUS_PAGE.value)
        )
)
@top_notification
async def groups_another_page(callback: CallbackQuery):
    offset: int = 0
    
    if callback.data.startswith(Commands.LOGIN_GROUPS_NEXT_PAGE.value):
        offset = int(callback.data.replace(Commands.LOGIN_GROUPS_NEXT_PAGE.value, ""))
    elif callback.data.startswith(Commands.LOGIN_GROUPS_PREVIOUS_PAGE.value):
        offset = int(callback.data.replace(Commands.LOGIN_GROUPS_PREVIOUS_PAGE.value, ""))

    await callback.message.edit_text(
        text="Выбери номер группы:",
        reply_markup=group_setter(
            groups=states[callback.message.chat.id].groups,
            offset=offset
        )
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_GROUP.value in callback.data
)
@top_notification
async def set_group(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting group
    callback_data = callback.data.split()
    
    (group_schedule_id, response_error) = get_group_schedule_id(group=callback_data[1])
    
    if group_schedule_id is None:
        await callback.message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        
        guards[callback.message.chat.id].drop()
        return
    
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    
    ExtendedStudents.update(
        group=callback_data[1],
        group_schedule_id=group_schedule_id,
        group_score_id=callback_data[2]
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    # Asking for name
    (group_names, response_error) = get_extended_login_data(extended_login_data_type=ExtendedLoginDataType.NAMES, user_id=user_id)
    
    if group_names is None:
        await callback.message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        
        guards[callback.message.chat.id].drop()
        return
    
    states[callback.message.chat.id].group_names = { name_id: name for (name, name_id) in group_names }
    
    await callback.message.edit_text(
        text="Выбери себя:",
        reply_markup=name_setter(names=list(states[callback.message.chat.id].group_names.items()))
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN_EXTENDED.value and (
            callback.data.startswith(Commands.LOGIN_NAMES_NEXT_PAGE.value) or
            callback.data.startswith(Commands.LOGIN_NAMES_PREVIOUS_PAGE.value)
        )
)
@top_notification
async def names_another_page(callback: CallbackQuery):
    offset: int = 0
    
    if callback.data.startswith(Commands.LOGIN_NAMES_NEXT_PAGE.value):
        offset = int(callback.data.replace(Commands.LOGIN_NAMES_NEXT_PAGE.value, ""))
    elif callback.data.startswith(Commands.LOGIN_NAMES_PREVIOUS_PAGE.value):
        offset = int(callback.data.replace(Commands.LOGIN_NAMES_PREVIOUS_PAGE.value, ""))

    await callback.message.edit_text(
        text="Выбери себя:",
        reply_markup=name_setter(
            names=list(states[callback.message.chat.id].group_names.items()),
            offset=offset
        )
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_NAME.value in callback.data
)
@top_notification
async def set_name(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting name
    name_id: str = callback.data.split()[1]
    
    ExtendedStudents.update(
        name=states[callback.message.chat.id].group_names[name_id],
        name_id=name_id
    ).where(
        ExtendedStudents.user_id == Users.get(Users.telegram_id == callback.message.chat.id).user_id
    ).execute()
    
    # Asking for student card number
    guard_message = await callback.message.edit_text(
        text=(
            "Отправь номер студенческого или зачётки.\n\n"
            "Если ты платник, нужно добавить большую букву *П* перед ним."
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Commands.LOGIN_SET_CARD.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        guards[message.chat.id].text == Commands.LOGIN_SET_CARD.value
)
async def set_card(message: Message):
    await message.delete()
    await guards[message.chat.id].message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    user_id: int = Users.get(Users.telegram_id == message.chat.id).user_id
    
    ExtendedStudents.update(
        card=message.text
    ).where(
        ExtendedStudents.user_id == user_id
    ).execute()
    
    (last_available_semester, response_error) = get_last_available_semester(user_id=user_id, is_card_check=True)
    
    if last_available_semester is None:
        await guards[message.chat.id].message.edit_text(
            text=response_error.value,
            reply_markup=canceler() if response_error is ResponseError.INCORRECT_CARD else None,
            disable_web_page_preview=True
        )
        
        if response_error is not ResponseError.INCORRECT_CARD:
            guards[message.chat.id].drop()
        
        return
    
    await finish_login(message=message)
