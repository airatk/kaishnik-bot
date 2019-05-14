from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.student import Student

from bot.constants import INSTITUTES
from bot.constants import REPLIES_TO_UNKNOWN_COMMAND

from bot.keyboards.settings import institute_setter
from bot.keyboards.settings import year_setter
from bot.keyboards.settings import group_number_setter
from bot.keyboards.settings import name_setter
from bot.keyboards.settings import set_card_skipper

from bot.helpers import save_to

from re import fullmatch


@kbot.callback_query_handler(func=lambda callback: callback.data == "first-setup")
@top_notification
def first_setup(callback):
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    except Exception:
        pass
    
    settings(callback.message)


@kbot.message_handler(
    commands=["settings"],
    func=lambda message:
        students[message.chat.id].previous_message == "/start" or
        students[message.chat.id].previous_message is None
)
@metrics.increment("settings")
def settings(message):
    students[message.chat.id].previous_message = "/settings"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="{warning}Выбери своё подразделение:".format(
            # Show the warning to the old users
            warning=(
                "Все текущие данные, включая "
                "*заметки*, *изменённое расписание* и *номер зачётки*, "
                "будут стёрты.\n\n" if not students[message.chat.id].is_not_set_up() else ""
            )
        ),
        reply_markup=institute_setter(is_old=not students[message.chat.id].is_not_set_up()),
        parse_mode="Markdown"
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message is not None and
        students[callback.message.chat.id].previous_message.startswith("/settings") and
        callback.data == "cancel-settings"
)
@top_notification
def cancel_setting_process(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отменено!"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        callback.data == "set-institute-КИТ"
)
@top_notification
def set_kit(callback):
    students[callback.message.chat.id] = Student(
        institute="КИТ",
        institute_id="КИТ",
        year="unknown",
        name="unknown",
        student_card_number="unknown"
    )
    
    students[callback.message.chat.id].previous_message = "/settings set-kit-group"  # Gate System (GS)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер своей группы."
    )


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/settings set-kit-group")
def set_kit_group_number(message):
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass
    
    if fullmatch("[4][1-4][2-5][0-9]", message.text):
        students[message.chat.id].group_number = message.text
    
        if students[message.chat.id].group_number is not None:
            students[message.chat.id].previous_message = None  # Gates System (GS)
            
            save_to(filename="data/users", object=students)
            
            kbot.send_message(
                chat_id=message.chat.id,
                text="Запомнено!"
            )
            kbot.send_message(
                chat_id=message.chat.id,
                text=REPLIES_TO_UNKNOWN_COMMAND[0],
                parse_mode="Markdown"
            )
        else:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
            
            students[message.chat.id] = Student()  # Drop all the entered data
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Неверный номер группы. Исправляйся."
        )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-institute-" in callback.data
)
@top_notification
def set_institute(callback):
    institute_id = callback.data.replace("set-institute-", "")
    
    students[callback.message.chat.id] = Student(
        institute=INSTITUTES[institute_id],
        institute_id=institute_id
    )
    
    students[callback.message.chat.id].previous_message = "/settings"  # Gates System (GS)
    
    years = students[callback.message.chat.id].get_dictionary_of(type="p_kurs")
    
    if years is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выбери свой курс:",
            reply_markup=year_setter(years)
        )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-year-" in callback.data
)
@top_notification
def set_year(callback):
    students[callback.message.chat.id].year = callback.data.replace("set-year-", "")
    
    groups = students[callback.message.chat.id].get_dictionary_of(type="p_group")
    
    if groups is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    
        students[callback.message.chat.id] = Student()  # Drop all the entered data
    elif groups != {}:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выбери свою группу:",
            reply_markup=group_number_setter(groups)
        )
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Здесь ничего нет. Начни сначала."
        )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-group-" in callback.data
)
@top_notification
def set_group_number(callback):
    students[callback.message.chat.id].group_number = callback.data.replace("set-group-", "")
    
    if students[callback.message.chat.id].group_number is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
    else:
        names = students[callback.message.chat.id].get_dictionary_of(type="p_stud")
        
        if names is None:
            kbot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Сайт kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
            
            students[callback.message.chat.id] = Student()  # Drop all the entered data
        elif names != {}:
            students[callback.message.chat.id].names = { name_id: name for name, name_id in names.items() }
            
            kbot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Выбери себя:",
                reply_markup=name_setter(names)
            )
        else:
            kbot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Здесь ничего нет. Начни сначала."
            )
            
            students[callback.message.chat.id] = Student()  # Drop all the entered data

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-name-" in callback.data
)
@top_notification
def set_name(callback):
    students[callback.message.chat.id].name = students[callback.message.chat.id].names[callback.data.replace("set-name-", "")]
    
    if students[callback.message.chat.id].name is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=(
                "Отправь номер своей зачётки "
                "(интересный факт — студенческий билет и зачётка имеют одинаковый номер!)."
                "\n\n"
                "Либо пропусти, но баллы показать не смогу."
            ),
            reply_markup=set_card_skipper()
        )
        
        students[callback.message.chat.id].previous_message = "/settings student-card-number"  # Gate System (GS)

@kbot.message_handler(
    func=lambda message:
        students[message.chat.id].previous_message == "/settings student-card-number" or
        students[message.chat.id].previous_message == "/card" and students[message.chat.id].student_card_number == "unset"
)
def set_student_card_number(message):
    students[message.chat.id].previous_message = "/settings student-card-number"  # Gate System (GS)
    
    if fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9][0-9]?", message.text):
        students[message.chat.id].student_card_number = message.text
        
        # The very 1st semester might be empty, so check the 1st one of the current year
        prelast_semester = int(students[message.chat.id].year)*2 - 1
        scoretable = students[message.chat.id].get_scoretable(prelast_semester)
        
        # Cleanning the chat
        try:
            kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        except Exception:
            pass
        
        if scoretable is None:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
        
            students[message.chat.id] = Student()  # Drop all the entered data
            
            return
        elif scoretable != []:
            students[message.chat.id].previous_message = None  # Gates System (GS)
            
            save_to(filename="data/users", object=students)
            
            kbot.send_message(
                chat_id=message.chat.id,
                text="Запомнено!"
            )
            kbot.send_message(
                chat_id=message.chat.id,
                text=REPLIES_TO_UNKNOWN_COMMAND[0],
                parse_mode="Markdown"
            )
            
            return
        else:
            students[message.chat.id].student_card_number = None
    else:
        # Cleanning the chat
        try:
            kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        except Exception:
            pass
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "Неверный номер зачётки. Исправляйся."
            "\n\n"
            "Либо пропусти, но баллы показать не смогу."
        ),
        reply_markup=set_card_skipper()
    )

@kbot.callback_query_handler(
    func=lambda callback: (
        students[callback.message.chat.id].previous_message == "/settings student-card-number" or
        students[callback.message.chat.id].previous_message == "/card"
    ) and callback.data == "skip-set-card"
)
@top_notification
def save_without_student_card_number(callback):
    students[callback.message.chat.id].student_card_number = "unset"
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    
    save_to(filename="data/users", object=students)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Запомнено без зачётки!"
    )
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text=REPLIES_TO_UNKNOWN_COMMAND[0],
        parse_mode="Markdown"
    )


@kbot.message_handler(
    func=lambda message:
        students[message.chat.id].previous_message is not None and
        students[message.chat.id].previous_message.startswith("/settings")
)
def gs_settings(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@kbot.callback_query_handler(func=lambda callback: students[callback.message.chat.id].is_not_set_up())
@top_notification
def deny_access_to_unsetup_callback(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    deny_access_to_unsetup_message(callback.message)

@kbot.message_handler(func=lambda message: students[message.chat.id].is_not_set_up())
@metrics.increment("unsetup")
def deny_access_to_unsetup_message(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "Настройка пройдена не полностью, исправляйся —\n"
            "/settings"
        )
    )
