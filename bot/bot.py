import telebot

import constants
import keyboards
import helpers
import student

import re
import random
import datetime

telebot.apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }
bot = telebot.TeleBot(constants.TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    student.students[message.chat.id] = student.Student()
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Для начала настрой меня на общение с тобой" + constants.EMOJI["smirking"],
        reply_markup=keyboards.settings_entry()
    )

@bot.message_handler(commands=["settings"])
def settings(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери свой институт (привет, ФМФ" + constants.EMOJI["moon"] + ").",
        reply_markup=keyboards.institute_setter()
    )

@bot.message_handler(func=lambda message: message.text in constants.INSTITUTES)
def set_institute(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    student.students[message.chat.id] = student.Student(constants.INSTITUTES[message.text])

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери свой курс.",
        reply_markup=keyboards.year_setter(student.students[message.chat.id].get_dict_of_list(type="p_kurs"))
    )

@bot.message_handler(func=lambda message: re.fullmatch("[1-6]", message.text))
def set_year(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_institute() is not None and \
       student.students[message.chat.id].get_year() is None:
        student.students[message.chat.id].set_year(message.text)
       
        groups = student.students[message.chat.id].get_dict_of_list(type="p_group")
       
        if groups:
            bot.send_message(
                chat_id=message.chat.id,
                text="Выбери свою группу.",
                reply_markup=keyboards.group_number_setter(groups)
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Здесь ничего нет. Начни сначала.",
                reply_markup=keyboards.settings_entry()
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(func=lambda message: re.fullmatch("[1-59][0-6][0-9][0-9]", message.text))
def set_group_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_year() is not None and \
       student.students[message.chat.id].get_group_number_for_schedule() is None:
        student.students[message.chat.id].set_group_number_for_score(message.text)
       
        names = student.students[message.chat.id].get_dict_of_list(type="p_stud")
       
        if names:
            student.students[message.chat.id].set_group_number_for_schedule(message.text)
            
            bot.send_message(
                chat_id=message.chat.id,
                text="Выбери себя.",
                reply_markup=keyboards.name_setter(names)
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Здесь ничего нет. Начни сначала.",
                reply_markup=keyboards.settings_entry()
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda message:
        message.chat.id in student.students and message.text in student.students[message.chat.id].get_dict_of_list(type="p_stud")
)
def set_name(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_group_number_for_schedule() is not None and \
       student.students[message.chat.id].get_name() is None:
        student.students[message.chat.id].set_name(message.text)

        bot.send_message(
            chat_id=message.chat.id,
            text="Отправь номер своей зачётки "
                 "(интересный факт - номер твоего студенческого и номер твоей зачётки одинаковы!).",
            parse_mode="Markdown",
            reply_markup=keyboards.remove_keyboard()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda message:
        re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9]", message.text) or
        re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9][0-9]", message.text)
)
def set_student_card_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_name() is not None and \
       student.students[message.chat.id].get_student_card_number() is None:
        student.students[message.chat.id].set_student_card_number(message.text)

        if student.students[message.chat.id].get_score_table(1):
            helpers.save_users(student.students)
            
            bot.send_message(
                chat_id=message.chat.id,
                text="Запомнено!",
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=constants.REPLIES_TO_UNKNOWN_COMMAND[0],
                parse_mode="Markdown"
            )
        else:
            student.students[message.chat.id].set_student_card_number(None)
        
            bot.send_message(
                chat_id=message.chat.id,
                text="Неверный номер зачётки. Исправляйся."
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды.",
            reply_markup=keyboards.settings_entry()
        )

@bot.message_handler(
    func=lambda message:
        student.students[message.chat.id].is_not_set_up() if message.chat.id in student.students else True
)
@bot.callback_query_handler(
    func=lambda callback:
        student.students[callback.message.chat.id].is_not_set_up() if callback.message.chat.id in student.students else True
)
def unsetup(callback):
    try:
        message = callback.message
    except:
        message = callback

    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Пройди настройку полностью.",
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
    todays_weekday = datetime.datetime.today().isoweekday()

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=student.students[callback.message.chat.id].get_schedule(
            type="classes",
            weekday=todays_weekday if callback.data == "today's" else todays_weekday + 1
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
    
    for weekday in constants.WEEK:
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=student.students[callback.message.chat.id].get_schedule(
                type="classes",
                weekday=weekday,
                next="next" in callback.data
            ),
            parse_mode="Markdown"
        )

@bot.message_handler(commands=["exams"])
def exams(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=student.students[message.chat.id].get_schedule(type="exams"),
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
        reply_markup=keyboards.semester_dailer(int(student.students[message.chat.id].get_year())*2 + 1)
    )

@bot.callback_query_handler(
    func=lambda callback:
        "s_r" in callback.data
)
def s_r(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери предмет:",
        reply_markup=keyboards.subject_chooser(
            score_table=student.students[callback.message.chat.id].get_score_table(callback.data[4:]),
            semester=callback.data[4:]
        )
    )

@bot.callback_query_handler(
    func=lambda callback:
        "s_t all" in callback.data
)
def show_score(callback):
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    callback_data = callback.data[8:].split()

    for subject in range(int(callback_data[0])):
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=helpers.get_subject_score(
                score_table=student.students[callback.message.chat.id].get_score_table(callback_data[1]),
                subjects_num=subject
            ),
            parse_mode="Markdown"
        )

@bot.callback_query_handler(
    func=lambda callback:
        "s_t" in callback.data
)
def show_score(callback):
    callback_data = callback.data[4:].split()

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=helpers.get_subject_score(
            score_table=student.students[callback.message.chat.id].get_score_table(callback_data[1]),
            subjects_num=int(callback_data[0])
        ),
        parse_mode="Markdown"
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
        text=constants.BUILDINGS[number]["description"],
        parse_mode="Markdown"
    )
    bot.send_location(
        chat_id=callback.message.chat.id,
        latitude=constants.BUILDINGS[number]["latitude"],
        longitude=constants.BUILDINGS[number]["longitude"]
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
    building = constants.LIBRARIES[number]["building"]
    
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=constants.LIBRARIES[number]["description"],
        parse_mode="Markdown"
    )
    bot.send_location(
        chat_id=callback.message.chat.id,
        latitude=constants.BUILDINGS[building]["latitude"],
        longitude=constants.BUILDINGS[building]["longitude"]
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
        text=constants.DORMS[number]["description"],
        parse_mode="Markdown"
    )
    bot.send_location(
        chat_id=callback.message.chat.id,
        latitude=constants.DORMS[number]["latitude"],
        longitude=constants.DORMS[number]["longitude"]
    )

@bot.message_handler(commands=["card"])
def card(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=student.students[message.chat.id].get_card(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.chat.id == constants.CREATOR and message.text == "What can I do?")
def creators_features(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=constants.CREATOR_CAN,
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda message: message.chat.id == constants.CREATOR,
    commands=["reverseweek"]
)
def reverseweek(message):
    helpers.reverse_week_in_file()
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Reversed."
    )

@bot.message_handler(
    func=lambda message: message.chat.id == constants.CREATOR,
    commands=["users"]
)
def users(message):
    helpers.reverse_week_in_file()
    
    bot.send_message(
        chat_id=message.chat.id,
        text="{users} users have tried me!".format(users=len(student.students))
    )

@bot.message_handler(func=lambda message: message.text[0] == "/")
def unknown_command(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.REPLIES_TO_UNKNOWN_COMMAND),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.message_handler(content_types=["text"])
def unknown_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown"
    )

bot.infinity_polling(True)
