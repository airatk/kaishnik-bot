from bot import kaishnik
from bot import students
from bot import metrics

from bot.student import Student

from bot.constants import INSTITUTES
from bot.constants import REPLIES_TO_UNKNOWN_COMMAND

from bot.keyboards import make_send
from bot.keyboards import institute_setter
from bot.keyboards import skipper
from bot.keyboards import remove_keyboard
from bot.keyboards import year_setter
from bot.keyboards import group_number_setter
from bot.keyboards import name_setter

from bot.helpers import save_users

from re import fullmatch
from json.decoder import JSONDecodeError

@kaishnik.message_handler(commands=["start"])
def start(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("start")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Для начала настрой меня на общение с тобой😏",
        reply_markup=make_send("/settings")
    )

@kaishnik.message_handler(commands=["settings"])
def settings(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("settings")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Выбери своё подразделение.",
        reply_markup=institute_setter()
    )
    
    # Show cancel option for old users
    if message.chat.id in students:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Или не выбирай:",
            reply_markup=skipper(
                text="отменить",
                callback_data="cancel"
            )
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        callback.data == "cancel"
)
def cancel_setting_process(callback):
    kaishnik.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id - 1
    )
    
    kaishnik.send_message(
        chat_id=callback.message.chat.id,
        text="Отменено!",
        reply_markup=remove_keyboard()
    )

@kaishnik.message_handler(
    func=lambda message:
        message.text == "КИТ"
)
def set_KIT(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Delete "cancel" message
    if message.chat.id in students:
        try:
            kaishnik.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id - 1
            )
        except Exception:
            pass

    students[message.chat.id] = Student(
        institute="КИТ",
        institute_id="КИТ",
        year="КИТ",
        name="КИТ",
        student_card_number="КИТ"
    )
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Отправь номер своей группы.",
        reply_markup=remove_keyboard()
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id in students and
        students[message.chat.id].institute_id == "КИТ" and
        fullmatch("[4][1-4][2-5][0-9]", message.text)
)
def set_KIT_group_number(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")

    if students[message.chat.id].group_number is None:
        try:
            students[message.chat.id].group_number_schedule = message.text
            students[message.chat.id].group_number = message.text
            # Reversed order to make sure there is no exception firstly
            
            save_users(students)
            
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Запомнено!"
            )
            kaishnik.send_message(
                chat_id=message.chat.id,
                text=REPLIES_TO_UNKNOWN_COMMAND[0],
                parse_mode="Markdown"
            )
        except IndexError:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Неверный номер группы. Исправляйся."
            )
        except JSONDecodeError:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
        )

@kaishnik.message_handler(
    func=lambda message:
        message.text in INSTITUTES
)
def set_institute(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Delete "cancel" message
    if message.chat.id in students:
        try:
            kaishnik.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id - 1
            )
        except Exception:
            pass
    
    students[message.chat.id] = Student(
        institute=message.text,
        institute_id=INSTITUTES[message.text]
    )

    try:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Выбери свой курс.",
            reply_markup=year_setter(students[message.chat.id].get_dictionary_of(type="p_kurs"))
        )
    except JSONDecodeError:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id in students and
        fullmatch("[1-6]", message.text)
)
def set_year(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    if students[message.chat.id].institute_id is not None and students[message.chat.id].year is None:
        students[message.chat.id].year = message.text
        
        try:
            groups = students[message.chat.id].get_dictionary_of(type="p_group")
            
            if groups:
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Выбери свою группу.",
                    reply_markup=group_number_setter(groups)
                )
            else:
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Здесь ничего нет. Начни сначала.",
                    reply_markup=make_send("/settings")
                )
        except JSONDecodeError:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
        )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id in students and
        students[message.chat.id].institute_id != "КИТ" and
        fullmatch("[1-59][0-6][0-9][0-9]", message.text)
)
def set_group_number(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    if students[message.chat.id].year is not None and students[message.chat.id].group_number is None:
        try:
            students[message.chat.id].group_number_score = message.text
            names = students[message.chat.id].get_dictionary_of(type="p_stud")
            
            if names:
                students[message.chat.id].group_number = message.text
                students[message.chat.id].group_number_schedule = message.text
                
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Выбери себя.",
                    reply_markup=name_setter(names)
                )
            else:
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Здесь ничего нет. Начни сначала.",
                    reply_markup=make_send("/settings")
                )
        except JSONDecodeError:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
        )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id in students and
        message.text in students[message.chat.id].get_dictionary_of(type="p_stud")
)
def set_name(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    if students[message.chat.id].group_number_schedule is not None and students[message.chat.id].name is None:
        students[message.chat.id].name = message.text
        students[message.chat.id].name_id = message.text
        
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Отправь номер своей зачётки "
                 "(интересный факт — номер твоего студенческого и номер твоей зачётки одинаковы!).",
            reply_markup=remove_keyboard()
        )
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
            reply_markup=skipper(
                text="пропустить",
                callback_data="skip"
            )
        )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды — отправь /settings",
        )

@kaishnik.callback_query_handler(
    func=lambda callback:
        callback.data == "skip"
)
def save_without_student_card_number(callback):
    students[callback.message.chat.id].student_card_number = "unset"
    save_users(students)
    
    # Might be undeleted sometimes for some reason
    try:
        kaishnik.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        kaishnik.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id - 1
        )
    except Exception:
        pass
    
    kaishnik.send_message(
        chat_id=callback.message.chat.id,
        text="Запомнено без зачётки!"
    )
    kaishnik.send_message(
        chat_id=callback.message.chat.id,
        text=REPLIES_TO_UNKNOWN_COMMAND[0],
        parse_mode="Markdown",
        reply_markup=remove_keyboard()
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id in students and
        fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9][0-9]?", message.text)
)
def set_student_card_number(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    if students[message.chat.id].name is not None and students[message.chat.id].student_card_number is None:
        students[message.chat.id].student_card_number = message.text
        
        # Delete "skip" message
        try:
            kaishnik.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id - 1
            )
        except Exception:
            pass
        
        # The 1st semester might be empty, so check the current one
        prelast_semester = int(students[message.chat.id].year)*2 - 1
        
        try:
            if students[message.chat.id].get_scoretable(prelast_semester):
                save_users(students)
                
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Запомнено!"
                )
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text=REPLIES_TO_UNKNOWN_COMMAND[0],
                    parse_mode="Markdown",
                    reply_markup=remove_keyboard()
                )
            else:
                students[message.chat.id].student_card_number = None
                
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Неверный номер зачётки. Исправляйся."
                )
                kaishnik.send_message(
                    chat_id=message.chat.id,
                    text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
                    reply_markup=skipper(
                        text="пропустить",
                        callback_data="skip"
                    )
                )
        except JSONDecodeError:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды — отправь /settings"
        )

@kaishnik.message_handler(
    func=lambda message:
        students[message.chat.id].is_not_set_up() if message.chat.id in students else True
)
@kaishnik.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].is_not_set_up() if callback.message.chat.id in students else True
)
def deny_access_to_unsetup(callback):
    try:
        message = callback.message
    except Exception:
        message = callback
    
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")

    metrics.increment("unsetup")

    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Пройди настройку полностью.",
        reply_markup=make_send("/settings")
    )
