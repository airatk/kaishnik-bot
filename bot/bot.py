import telebot

import secrets
import constants
import keyboards
import helpers
import student

import re
import random

telebot.apihelper.proxy = secrets.PROXY
bot = telebot.TeleBot(secrets.TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Для начала настрой меня на общение с тобой" + constants.emoji["smirking"],
        reply_markup=keyboards.settings_entry()
    )

@bot.message_handler(commands=["classes"])
def classes(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Тебе нужно расписание на:",
        reply_markup=keyboards.schedule_type()
    )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "today's" or callback.data == "tomorrow's"
)
def one_day_schedule(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=helpers.get_schedule(
            type="classes",
            kind=callback.data
        ),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(
    func=lambda callback:
        "weekly" in callback.data
)
def weekly_schedule(callback):
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    for weekday in constants.week:
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=helpers.get_schedule(
                type="classes",
                kind=weekday,
                next="next" in callback.data
            ),
            parse_mode="Markdown"
        )

@bot.message_handler(commands=["exams"])
def exams(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=helpers.get_schedule(
            type="exams",
            kind=None,
            group_number=student.student.get_group_number()
        ),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["week"])
def week(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=helpers.get_week()
    )

@bot.message_handler(commands=["score"])
def score(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери номер семестра:",
        reply_markup=keyboards.semester_dailer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        "s_r" in callback.data
)
def s_r(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери предмет:" #if is_semester else "Этот семестр пока не доступен.",
        # TODO: implement the thing below
        # reply_markup=keyboards.subject_chooser()
    )

@bot.message_handler(commands=["locations"])
def locations(message):
    bot.send_chat_action(chat_id=message.chat.id, action="find_location")

    bot.send_message(
        chat_id=message.chat.id,
        text="Аж три варианта на выбор:",
        reply_markup=keyboards.choose_location_type()
    )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "buildings"
)
def b_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 8 учебных зданий и 1 спортивный комплекс:",
        reply_markup=keyboards.buildings_dailer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        "b_s" in callback.data
)
def send_building(callback):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = callback.data[4:]

    bot.send_message(
        chat_id=callback.message.chat.id,
        text=constants.buildings[number]["description"],
        parse_mode="Markdown"
    )
    bot.send_location(
        chat_id=callback.message.chat.id,
        latitude=constants.buildings[number]["latitude"],
        longitude=constants.buildings[number]["longitude"]
    )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "libraries"
)
def l_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 5 библиотек:",
        reply_markup=keyboards.libraries_dailer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        "l_s" in callback.data
)
def send_library(callback):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = callback.data[4:]
    building = constants.libraries[number]["building"]
    
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=constants.libraries[number]["description"],
        parse_mode="Markdown"
    )
    bot.send_location(
        chat_id=callback.message.chat.id,
        latitude=constants.buildings[building]["latitude"],
        longitude=constants.buildings[building]["longitude"]
    )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "dorms"
)
def d_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 7 общежитий:",
        reply_markup=keyboards.dorms_dailer()
    )

@bot.callback_query_handler(
    func=lambda callback:
        "d_s" in callback.data
)
def send_dorm(callback):
    bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    number = callback.data[4:]

    bot.send_message(
        chat_id=callback.message.chat.id,
        text=constants.dorms[number]["description"],
        parse_mode="Markdown"
    )
    bot.send_location(
        chat_id=callback.message.chat.id,
        latitude=constants.dorms[number]["latitude"],
        longitude=constants.dorms[number]["longitude"]
    )

@bot.message_handler(commands=["settings"])
def settings(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери свой институт (привет, ФМФ" + constants.emoji["moon"] + ").",
        reply_markup=keyboards.institute_setter()
    )

@bot.message_handler(
    func=lambda m:
        m.text in constants.institutes
)
def set_institute(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    student.student = student.Student(constants.institutes[message.text])

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери свой курс.",
        reply_markup=keyboards.year_setter()
    )

@bot.message_handler(
    func=lambda m:
        True if re.fullmatch("[1-6]", m.text) else False
)
def set_year(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.student.get_institute() is not None and \
       student.student.get_year() is None:
        student.student.set_year(message.text)

        bot.send_message(
            chat_id=message.chat.id,
            text="Выбери свою группу.",
            reply_markup=keyboards.group_number_setter()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda m:
        True if re.fullmatch("[1-59][1-6][0-9][0-9]", m.text) else False
)
def set_group_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.student.get_institute() is not None and \
       student.student.get_year() is not None and \
       student.student.get_group_number_for_schedule() is None:
        student.student.set_group_number_for_schedule(message.text)
        student.student.set_group_number_for_score(message.text)

        bot.send_message(
            chat_id=message.chat.id,
            text="Выбери себя.",
            reply_markup=keyboards.name_setter()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda m:
        student.student.get_institute() is not None and \
        student.student.get_year() is not None and \
        student.student.get_group_number_for_score() is not None and \
        m.text in helpers.get_dict_of_list(
            type="p_stud",
            params=(
                ("p_fac", student.student.get_institute()),
                ("p_kurs", student.student.get_year()),
                ("p_group", student.student.get_group_number_for_score())
            )
        )
)
def set_name(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.student.get_institute() is not None and \
       student.student.get_year() is not None and \
       student.student.get_group_number_for_schedule() is not None and \
       student.student.get_name() is None:
        student.student.set_name(message.text)

        bot.send_message(
            chat_id=message.chat.id,
            text="Отправь номер своей зачётки в формате: 123456 (интересный факт - номер твоего студенческого и номер твоей зачётки одинаковы!).",
            reply_markup=keyboards.remove_keyboard()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda m:
        True if re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9]", m.text) else False
)
def set_student_card_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.student.get_institute() is not None and \
       student.student.get_year() is not None and \
       student.student.get_group_number_for_score() is not None and \
       student.student.get_name() is not None and \
       student.student.get_student_card_number() is None:
        student.student.set_student_card_number(message.text)

        bot.send_message(
            chat_id=message.chat.id,
            text="Запомнено!",
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=constants.replies_to_unknown_command[0], # Coincidencially this string is on replies_to_unknown_command list :)
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda m:
        m.chat.id == secrets.CREATOR and m.text == "What can I do?"
)
def creators_features(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=constants.YOU_CAN,
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda m:
        m.chat.id == secrets.CREATOR,
    commands=["reverseweek"]
)
def reverseweek(message):
    helpers.reverse_week_in_file()
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Reversed."
    )

@bot.message_handler(
    func=lambda m:
        m.text[0] == "/"
)
def unknown_command(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.replies_to_unknown_command),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.message_handler(content_types=["text"])
def unknown_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.replies_to_unknown_message),
        parse_mode="Markdown"
    )

bot.polling()
