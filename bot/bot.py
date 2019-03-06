import telebot

import constants
import keyboards
import helpers
import student

import re
import random
import datetime

telebot.apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }
bot = telebot.TeleBot(constants.TOKEN, threaded=False)

@bot.message_handler(
    content_types=[
        "sticker",
        "photo", "video", "audio", "document",
        "voice", "video_note", "location", "contact"
    ]
)
def unknown_nontext_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Йоу!"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Для начала настрой меня на общение с тобой" + constants.EMOJI["smirking"],
        reply_markup=keyboards.make_send("/settings")
    )

@bot.message_handler(commands=["settings"])
def settings(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери своё подразделение.",
        reply_markup=keyboards.institute_setter()
    )

    # Show cancel option for old users
    if message.chat.id in student.students:
        bot.send_message(
            chat_id=message.chat.id,
            text="Или не выбирай:",
            reply_markup=keyboards.skipper(
                text="отменить",
                callback_data="cancel"
            )
        )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "cancel"
)
def cancel_setting_process(callback):
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id - 1
    )
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    bot.send_message(
        chat_id=callback.message.chat.id,
        text="Отменено!",
        reply_markup=keyboards.remove_keyboard()
    )

@bot.message_handler(
    func=lambda message:
        message.text == "КИТ"
)
def set_KIT(message):
    student.students[message.chat.id] = student.Student(
        institute="КИТ",
        year="КИТ",
        group_number_for_score="КИТ",
        name="КИТ",
        student_card_number="КИТ",
    )

    bot.send_message(
        chat_id=message.chat.id,
        text="Отправь номер своей группы.",
        reply_markup=keyboards.remove_keyboard()
    )

@bot.message_handler(
    func=lambda message:
        message.chat.id in student.students and \
        student.students[message.chat.id].get_institute() == "КИТ" and \
        re.fullmatch("[4][1-4][2-5][0-9]", message.text)
)
def set_KIT_group_number(message):
    if student.students[message.chat.id].get_group_number_for_schedule() is None:
        try:
            student.students[message.chat.id].set_group_number_for_schedule(message.text)

            helpers.save_users(student.students)
            
            bot.send_message(
                chat_id=message.chat.id,
                text="Запомнено!"
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=constants.REPLIES_TO_UNKNOWN_COMMAND[0],
                parse_mode="Markdown"
            )
        except IndexError:
            bot.send_message(
                chat_id=message.chat.id,
                text="Неверный номер группы. Исправляйся."
            )
        except:
            bot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
        )

@bot.message_handler(
    func=lambda message:
        message.text in constants.INSTITUTES
)
def set_institute(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if message.chat.id in student.students:
        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id - 1
            )  # Delete "cancel" message
        except:
            pass

    student.students[message.chat.id] = student.Student(institute=constants.INSTITUTES[message.text])

    try:
        bot.send_message(
            chat_id=message.chat.id,
            text="Выбери свой курс.",
            reply_markup=keyboards.year_setter(student.students[message.chat.id].get_dict_of_list(type="p_kurs"))
        )
    except:
        bot.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@bot.message_handler(
    func=lambda message:
        message.chat.id in student.students and \
        re.fullmatch("[1-6]", message.text)
)
def set_year(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_institute() is not None and \
       student.students[message.chat.id].get_year() is None:
        student.students[message.chat.id].set_year(message.text)
       
        try:
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
                    reply_markup=keyboards.make_send("/settings")
                )
        except:
            bot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
        )

@bot.message_handler(
    func=lambda message:
        message.chat.id in student.students and \
        not student.students[message.chat.id].get_institute() == "КИТ" and \
        re.fullmatch("[1-59][0-6][0-9][0-9]", message.text)
)
def set_group_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_year() is not None and \
       student.students[message.chat.id].get_group_number_for_schedule() is None:
        student.students[message.chat.id].set_group_number_for_score(message.text)
       
        try:
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
                    reply_markup=keyboards.make_send("/settings")
                )
        except:
            bot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
        )

@bot.message_handler(
    func=lambda message:
        message.chat.id in student.students and \
        message.text in student.students[message.chat.id].get_dict_of_list(type="p_stud")
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
            reply_markup=keyboards.remove_keyboard()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
            reply_markup=keyboards.skipper(
                text="пропустить",
                callback_data="skip"
            )
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings",
        )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "skip"
)
def without_student_card_number(callback):
    helpers.save_users(student.students)
    
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id - 1
    )
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Запомнено без зачётки!"
    )
    bot.send_message(
        chat_id=callback.message.chat.id,
        text=constants.REPLIES_TO_UNKNOWN_COMMAND[0],
        parse_mode="Markdown",
        reply_markup=keyboards.remove_keyboard()
    )

@bot.message_handler(
    func=lambda message:
        message.chat.id in student.students and ( \
            re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9]", message.text) or \
            re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9][0-9]", message.text) \
        )
)
def set_student_card_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if student.students[message.chat.id].get_name() is not None and \
       student.students[message.chat.id].get_student_card_number() is None:
        student.students[message.chat.id].set_student_card_number(message.text)

        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id - 1
            )  # Delete "skip" message
        except:
            pass

        # Because the first semester might be empty
        prelast_semester = int(student.students[message.chat.id].get_year())*2 - 1
        
        try:
            if student.students[message.chat.id].get_score_table(prelast_semester):
                helpers.save_users(student.students)
                
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Запомнено!"
                )
                bot.send_message(
                    chat_id=message.chat.id,
                    text=constants.REPLIES_TO_UNKNOWN_COMMAND[0],
                    parse_mode="Markdown",
                    reply_markup=keyboards.remove_keyboard()
                )
            else:
                student.students[message.chat.id].set_student_card_number(None)
            
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Неверный номер зачётки. Исправляйся."
                )
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
                    reply_markup=keyboards.skipper(
                        text="пропустить",
                        callback_data="skip"
                    )
                )
        except:
            bot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
                disable_web_page_preview=True
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Если хочешь изменить настройки, начни с соответствующей команды - отправь /settings"
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
        reply_markup=keyboards.make_send("/settings")
    )

@bot.message_handler(commands=["lecturers"])
def lecturers(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Введи ФИО преподавателя полностью или частично."
    )

    student.students[message.chat.id].set_pmt(message.text)

@bot.message_handler(
    func=lambda message:
        student.students[message.chat.id].get_pmt() == "/lecturers",
    content_types=["text"]
)
def find_lecturer(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # In case kai.ru is down
    try:
        names = helpers.get_lecturers_names(message.text)
    except:
        names = None

    if names:
        try:
            bot.send_message(
                chat_id=message.chat.id,
                text="Выбери преподавателя:",
                reply_markup=keyboards.choose_lecturer(names)
            )
        except:
            bot.send_message(
                chat_id=message.chat.id,
                text="Слишком мало букв, слишком много преподавателей…"
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Ничего не найдено :("
        )
    
    student.students[message.chat.id].set_pmt(None)

@bot.callback_query_handler(
    func=lambda callback:
        "l_r" in callback.data
)
def send_lecturers_schedule(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужно преподавателево расписание:",
        reply_markup=keyboards.lecturer_schedule_type(callback.data[4:])
    )

@bot.callback_query_handler(
    func=lambda callback:
        "l_c" in callback.data or \
        "l_e" in callback.data
)
def send_lecturers_schedule(callback):
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    try:
        if "l_c" in callback.data:
            for weekday in constants.WEEK:
                bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=helpers.get_lecturers_schedule(
                        prepod_login=callback.data[4:],
                        type=callback.data[:3],
                        weekday=weekday
                    ),
                    parse_mode="Markdown"
                )
        else:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text=helpers.get_lecturers_schedule(
                    prepod_login=callback.data[4:],
                    type=callback.data[:3]
                ),
                parse_mode="Markdown"
            )
    except:
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
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
        callback.data == "today's" or \
        callback.data == "tomorrow's"
)
def one_day_schedule(callback):
    todays_weekday = datetime.datetime.today().isoweekday()

    try:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=student.students[callback.message.chat.id].get_schedule(
                type="classes",
                weekday=todays_weekday if callback.data == "today's" else todays_weekday + 1
            ),
            parse_mode="Markdown"
        )
    except:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
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
    
    try:
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
    except:
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@bot.message_handler(commands=["exams"])
def exams(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        bot.send_message(
            chat_id=message.chat.id,
            text=student.students[message.chat.id].get_schedule(type="exams"),
            parse_mode="Markdown"
        )
    except:
        bot.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
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
    
    if student.students[message.chat.id].get_student_card_number() is None:
        bot.send_message(
            chat_id=message.chat.id,
            text="Номер зачётки не указан, но ты можешь это исправить - отправь /card"
        )
    elif student.students[message.chat.id].get_institute() == "КИТ":
        bot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
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
    try:
        # There might be no data for the certain semester
        if student.students[callback.message.chat.id].get_score_table(callback.data[4:]) is None:
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Нет данных."
            )
        else:
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Выбери предмет:",
                reply_markup=keyboards.subject_chooser(
                    score_table=student.students[callback.message.chat.id].get_score_table(callback.data[4:]),
                    semester=callback.data[4:]
                )
            )
    except:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@bot.callback_query_handler(
    func=lambda callback:
        "s_t all" in callback.data
)
def show_all_score(callback):
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    callback_data = callback.data[8:].split()

    try:
        for subject in range(int(callback_data[0])):
            bot.send_message(
                chat_id=callback.message.chat.id,
                text=helpers.get_subject_score(
                    score_table=student.students[callback.message.chat.id].get_score_table(callback_data[1]),
                    subjects_num=subject
                ),
                parse_mode="Markdown"
            )
    except:
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@bot.callback_query_handler(
    func=lambda callback:
        "s_t" in callback.data
)
def show_score(callback):
    callback_data = callback.data[4:].split()

    try:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=helpers.get_subject_score(
                score_table=student.students[callback.message.chat.id].get_score_table(callback_data[1]),
                subjects_num=int(callback_data[0])
            ),
            parse_mode="Markdown"
        )
    except:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Сайт kai.ru не отвечает ¯\_(ツ)_/¯",
            disable_web_page_preview=True
        )

@bot.message_handler(commands=["locations"])
def locations(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

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
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")

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
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")

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
    bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")

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

    if student.students[message.chat.id].get_student_card_number() is None:
        bot.send_message(
            chat_id=message.chat.id,
            text="Отправь номер своей зачётки "
                 "(интересный факт - номер твоего студенческого и номер твоей зачётки одинаковы!).",
            reply_markup=keyboards.remove_keyboard()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
            reply_markup=keyboards.skipper(
                text="пропустить",
                callback_data="skip"
            )
        )
    elif student.students[message.chat.id].get_institute() == "КИТ":
        bot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=student.students[message.chat.id].get_card(),
            parse_mode="Markdown"
        )

@bot.message_handler(commands=["brs"])
def brs(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=constants.BRS,
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda message:
        message.chat.id == constants.CREATOR and \
        message.text == "What can I do?"
)
def creators_features(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=constants.CREATOR_CAN,
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda message:
        message.chat.id == constants.CREATOR,
    commands=["users"]
)
def users(message):
    institutes_statistics = [student.students[user].get_institute() for user in student.students]
    year_statistics = [student.students[user].get_year() for user in student.students]

    bot.send_message(
        chat_id=message.chat.id,
        text="*Institutes*\n" \
             "• ИАНТЭ: {}\n" \
             "• ФМФ: {}\n" \
             "• ИАЭП: {}\n" \
             "• ИКТЗИ: {}\n" \
             "• КИТ: {}\n" \
             "• ИРЭТ: {}\n" \
             "• ИЭУСТ: {}\n" \
             "\n*Years*\n" \
             "• 1: {}\n" \
             "• 2: {}\n" \
             "• 3: {}\n" \
             "• 4: {}\n" \
             "• 5: {}\n" \
             "• 6: {}\n\n" \
             "*{}* users in total!".format(
                 institutes_statistics.count(constants.INSTITUTES["ИАНТЭ"]),
                 institutes_statistics.count(constants.INSTITUTES["ФМФ"]),
                 institutes_statistics.count(constants.INSTITUTES["ИАЭП"]),
                 institutes_statistics.count(constants.INSTITUTES["ИКТЗИ"]),
                 institutes_statistics.count(constants.INSTITUTES["КИТ"]),
                 institutes_statistics.count(constants.INSTITUTES["ИРЭТ"]),
                 institutes_statistics.count(constants.INSTITUTES["ИЭУСТ"]),
                 year_statistics.count("1"),
                 year_statistics.count("2"),
                 year_statistics.count("3"),
                 year_statistics.count("4"),
                 year_statistics.count("5"),
                 year_statistics.count("6"),
                 len(student.students)
        ),
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda message:
        message.chat.id == constants.CREATOR,
    commands=["clear"]
)
def clear(message):  # Deleting users who doesn't use the bot
    is_someone_cleared = False

    for user in list(student.students):
        try:
            bot.send_chat_action(chat_id=user, action="upload_document")
        except:
            is_someone_cleared = True
        
            bot.send_message(
                chat_id=message.chat.id,
                text="{first_name} {last_name} (@{user}) stopped using the bot, so was #erased.\n\n" \
                     "Institute: {institute}\n" \
                     "Year: {year}\n" \
                     "Student card number: {student_card_number}".format(
                         first_name=bot.get_chat(chat_id=user).first_name,
                         last_name=bot.get_chat(chat_id=user).last_name,
                         user=bot.get_chat(chat_id=user).username,
                         institute=student.students[user].get_institute(),
                         year=student.students[user].get_year(),
                         student_card_number=student.students[user].get_student_card_number()
                ),
                parse_mode="Markdown"
            )
            
            del student.students[user]

    helpers.save_users(student.students)

    if is_someone_cleared:
        bot.send_message(
            chat_id=message.chat.id,
            text="Cleared!"
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="No one has stopped using the bot!"
        )

@bot.message_handler(
    func=lambda message:
        message.chat.id == constants.CREATOR,
    commands=["drop"]
)
def drop(message):
    helpers.save_users(dict())

    bot.send_message(
        chat_id=message.chat.id,
        text="Dropped!"
    )

@bot.message_handler(
    func=lambda message:
        message.chat.id == constants.CREATOR,
    commands=["broadcast"]
)
def broadcast(message):
    for user in student.students:
        try:
            bot.send_message(
                chat_id=user,
                text="*Телеграмма от разработчика*\n\n" +
                     message.text[11:] +
                     "\n\nНаписать разработчику: @airatk",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except:
            pass  # Do nothing with a user who blocked the bot. Right, just leave him

@bot.message_handler(
    func=lambda message:
        message.chat.id == constants.CREATOR,
    commands=["reverseweek"]
)
def reverseweek(message):
    helpers.reverse_week_in_file()
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Reversed."
    )

@bot.message_handler(
    func=lambda message:
        message.text[0] == "/"
)
def unknown_command(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.REPLIES_TO_UNKNOWN_COMMAND),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.message_handler(content_types=["text"])
def unknown_text_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(constants.REPLIES_TO_UNKNOWN_MESSAGE),
        parse_mode="Markdown"
    )

bot.infinity_polling(True)
