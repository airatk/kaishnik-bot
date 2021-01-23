from random import choice

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot import dispatcher
from bot import guards
from bot import states

from bot.commands.login.menu import finish_login
from bot.commands.login.utilities.keyboards import institute_setter
from bot.commands.login.utilities.keyboards import year_setter
from bot.commands.login.utilities.keyboards import group_setter
from bot.commands.login.utilities.keyboards import name_setter

from bot.models.users import Users
from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents

from bot.utilities.keyboards import canceler
from bot.utilities.helpers import top_notification
from bot.utilities.constants import BOT_ADDRESSING
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
    institute_id: int = callback.data.split()[1]
    
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
        return
    
    await callback.message.edit_text(
        text="Выбери номер группы:",
        reply_markup=group_setter(groups)
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
        await callback.message.edit_text(text=response_error.value)
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
        return
    
    states[callback.message.chat.id].group_names = { name_id: name for (name, name_id) in group_names.items() }
    
    await callback.message.edit_text(
        text="Выбери себя:",
        reply_markup=name_setter(names=group_names)
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
        ExtendedStudents.user_id == Users.get(
            Users.telegram_id == callback.message.chat.id
        ).user_id
    ).execute()
    
    # Asking for student card number
    guard_message = await callback.message.edit_text(
        text="Отправь номер студенческого или зачётки.",
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Commands.LOGIN_SET_CARD.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and
        message.text is not None and message.text.startswith(BOT_ADDRESSING) and
        guards[message.chat.id].text == Commands.LOGIN_SET_CARD.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Commands.LOGIN_SET_CARD.value
)
async def set_card(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text[len(BOT_ADDRESSING):]
    
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
    
    (last_available_semester, response_error) = get_last_available_semester(user_id=user_id)
    
    if last_available_semester is None:
        await guards[message.chat.id].message.edit_text(
            text=response_error.value,
            reply_markup=canceler() if response_error is ResponseError.INCORRECT_CARD else None,
            disable_web_page_preview=True
        )
        return
    
    await finish_login(message=message)
