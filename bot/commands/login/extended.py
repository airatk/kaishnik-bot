from bot import bot
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


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN.value and
        callback.data == Commands.LOGIN_EXTENDED.value
)
@top_notification
def login_extended(callback):
    # Resetting the user
    students[callback.message.chat.id] = Student()
    
    students[callback.message.chat.id].is_setup = False
    students[callback.message.chat.id].is_full = True
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери институт (привет, ФМФ🌚):",
        reply_markup=institute_setter()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_EXTENDED.value

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_INSTITUTE.value in callback.data
)
@top_notification
def set_institute(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting institute
    institute_id = callback.data.split()[1]
    
    students[callback.message.chat.id].institute = INSTITUTES[institute_id]
    students[callback.message.chat.id].institute_id = institute_id
    
    # Asking for year
    years = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.YEARS)
    
    if len(years) == 0:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери курс:",
        reply_markup=year_setter(years)
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_YEAR.value in callback.data
)
@top_notification
def set_year(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting year
    students[callback.message.chat.id].year = callback.data.split()[1]
    
    # Asking for group
    groups = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.GROUPS)
    
    if len(groups) == 0:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери группу:",
        reply_markup=group_number_setter(groups)
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_GROUP.value in callback.data
)
@top_notification
def set_group(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting group
    students[callback.message.chat.id].group = callback.data.split()[1]
    
    if students[callback.message.chat.id].group_schedule_id is None and students[callback.message.chat.id].group_score_id is not None:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_GROUP.value
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    if students[callback.message.chat.id].group_score_id is None:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    # Asking for name
    names = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.NAMES)
    
    if len(names) == 0:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    students[callback.message.chat.id].names = { name_id: name for (name, name_id) in names.items() }
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери себя:",
        reply_markup=name_setter(names)
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_EXTENDED.value and
        Commands.LOGIN_SET_NAME.value in callback.data
)
@top_notification
def set_name(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    # Setting name
    name = callback.data.split()[1]
    students[callback.message.chat.id].name = students[callback.message.chat.id].names[name]
    
    if students[callback.message.chat.id].name_id is None:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    # Asking for student card number
    guard_message = bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер зачётки.",
        reply_markup=cancel_option()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_SET_CARD.value
    students[callback.message.chat.id].guard.message = guard_message

@bot.message_handler(func=lambda message: students[message.chat.id].guard.text == Commands.LOGIN_SET_CARD.value)
def set_card(message):
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[message.chat.id].card = message.text
    last_available_semester = students[message.chat.id].get_last_available_semester()
    
    if last_available_semester is None:
        bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        return
    
    if last_available_semester == 0:
        bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text=ResponseError.INCORRECT_CARD.value,
            reply_markup=cancel_option()
        )
        
        students[message.chat.id].card = None
        return
    
    bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text="Запомнено!"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=GUIDE_MESSAGE,
        parse_mode="Markdown"
    )
    
    students[message.chat.id].guard.drop()
    students[message.chat.id].is_setup = True
    save_data(file=USERS_FILE, object=students)
