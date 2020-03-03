from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher
from bot import students

from bot.commands.login.utilities.keyboards import institute_setter
from bot.commands.login.utilities.keyboards import year_setter
from bot.commands.login.utilities.keyboards import group_number_setter
from bot.commands.login.utilities.keyboards import name_setter
from bot.commands.login.utilities.constants import GUIDE_MESSAGE

from bot.shared.keyboards import cancel_option
from bot.shared.helpers import top_notification
from bot.shared.api.constants import INSTITUTES
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ScoreDataType
from bot.shared.api.types import ResponseError
from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands

from random import choice


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN.value and
        callback.data == Commands.LOGIN_EXTENDED.value
)
@top_notification
async def login_extended(callback: CallbackQuery):
    # Resetting the user
    students[callback.message.chat.id] = Student()
    
    students[callback.message.chat.id].is_setup = False
    students[callback.message.chat.id].is_full = True
    
    await callback.message.edit_text(
        text="Выбери институт (привет, ФМФ🌚):",
        reply_markup=institute_setter()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_EXTENDED.value

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
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
    
    students[callback.message.chat.id].institute = INSTITUTES[institute_id]
    students[callback.message.chat.id].institute_id = institute_id
    
    # Asking for year
    years: {str: str} = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.YEARS)
    
    if len(years) == 0:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    await callback.message.edit_text(
        text="Выбери курс:",
        reply_markup=year_setter(years)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_YEAR.value in callback.data
)
@top_notification
async def set_year(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting year
    students[callback.message.chat.id].year = callback.data.split()[1]
    
    # Asking for group
    groups: {str: str} = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.GROUPS)
    
    if len(groups) == 0:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    await callback.message.edit_text(
        text="Выбери группу:",
        reply_markup=group_number_setter(groups)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_GROUP.value in callback.data
)
@top_notification
async def set_group(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting group
    students[callback.message.chat.id].group = callback.data.split()[1]
    
    if students[callback.message.chat.id].group_schedule_id is None and students[callback.message.chat.id].group_score_id is not None:
        await callback.message.edit_text(text=ResponseError.NO_GROUP.value)
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    if students[callback.message.chat.id].group_score_id is None:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    # Asking for name
    names: {str: str} = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.NAMES)
    
    if len(names) == 0:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    students[callback.message.chat.id].names = { name_id: name for (name, name_id) in names.items() }
    
    await callback.message.edit_text(
        text="Выбери себя:",
        reply_markup=name_setter(names)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_NAME.value in callback.data
)
@top_notification
async def set_name(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting name
    name: str = callback.data.split()[1]
    students[callback.message.chat.id].name = students[callback.message.chat.id].names[name]
    
    if students[callback.message.chat.id].name_id is None:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    # Asking for student card number
    guard_message = await callback.message.edit_text(
        text="Отправь номер зачётки.",
        reply_markup=cancel_option()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_SET_CARD.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.message_handler(lambda message: students[message.chat.id].guard.text == Commands.LOGIN_SET_CARD.value)
async def set_card(message: Message):
    await message.delete()
    await students[message.chat.id].guard.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[message.chat.id].card = message.text
    last_available_semester: int = students[message.chat.id].get_last_available_semester()
    
    if last_available_semester is None:
        await students[message.chat.id].guard.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        return
    
    if last_available_semester == 0:
        await students[message.chat.id].guard.message.edit_text(
            text=ResponseError.INCORRECT_CARD.value,
            reply_markup=cancel_option()
        )
        
        students[message.chat.id].card = None
        return
    
    await students[message.chat.id].guard.message.edit_text(text="Запомнено!")
    
    await message.answer(
        text=GUIDE_MESSAGE,
        parse_mode="markdown"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].is_setup = True
    
    save_data(file=USERS_FILE, object=students)
