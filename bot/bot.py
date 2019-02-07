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
        text="Тебе нужно расписание на",
        reply_markup=keyboards.schedule_type()
    )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "today's" or callback.data == "tomorrow's"
)
def daily_schedule(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=helpers.get_schedule(
            type="classes",
            kind=callback.data,
            group_number=student.student.get_group_number()
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
    
    for weekday in range(1, 7):
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=helpers.get_schedule(
                type="classes",
                kind=weekday,
                group_number=student.student.get_group_number(),
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

    pass

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

    if "first" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Первый дом*\n\n"
                 "Ближайшая остановка: КАИ.\n"
                 "Есть буфет и читальный зал №1.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["first"]["latitude"],
            longitude=constants.buildings["first"]["longitude"]
        )
    elif "second" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*2ка*\n\n"
                 "Ближайшие остановки: Четаева, Чистопольская, Амирхана, СК Олимп.\n"
                 "Есть буфет.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["second"]["latitude"],
            longitude=constants.buildings["second"]["longitude"]
        )
    elif "third" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*3ка*\n\n"
                 "Ближайшие остановки: Толстого и Гоголя.\n"
                 "Есть буфет и читальный зал №3.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["third"]["latitude"],
            longitude=constants.buildings["third"]["longitude"]
        )
    elif "fourth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*4ка*\n\n"
                 "Ближайшие остановки: Толстого и Гоголя.\n"
                 "Ни буфета, ни читального зала - грустно!",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["fourth"]["latitude"],
            longitude=constants.buildings["fourth"]["longitude"]
        )
    elif "fifth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*5ка*\n\n"
                 "Ближайшая остановка: Площадь Свободы.\n"
                 "Есть столовая и читальный зал №2.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["fifth"]["latitude"],
            longitude=constants.buildings["fifth"]["longitude"]
        )
    elif "sixth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*6ка*\n\n"
                 "Ближайшие остановки: Институт, Кошевого, КМПО.\n"
                 "Есть буфет.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["sixth"]["latitude"],
            longitude=constants.buildings["sixth"]["longitude"]
        )
    elif "seventh" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*7ка*\n\n"
                 "Ближайшие остановки: Гоголя и Толстого.\n"
                 "Есть буфет и читальный зал №9.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["seventh"]["latitude"],
            longitude=constants.buildings["seventh"]["longitude"]
        )
    elif "eighth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*8ка*\n\n"
                 "Ближайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.\n"
                 "Есть буфет и научно-техническая библиотека.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["eighth"]["latitude"],
            longitude=constants.buildings["eighth"]["longitude"]
        )
    elif "olymp" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*СК Олимп*\n\n"
                 "Ближайшие остановки: СК Олимп, Чистопольская, Четаева, Амирхана.\n"
                 "На самом деле, у Олимпа два здания: основное и здание бассейна, а ещё есть стадион.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["olymp"]["latitude"],
            longitude=constants.buildings["olymp"]["longitude"]
        )

@bot.callback_query_handler(
    func=lambda callback:
        callback.data == "libraries"
)
def b_s(callback):
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

    if "first" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Читальный зал №1*\n\n"
                 "Ближайшая остановка: КАИ.\n"
                 "В первом доме.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["first"]["latitude"],
            longitude=constants.buildings["first"]["longitude"]
        )
    elif "second" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Читальный зал №2*\n\n"
                 "Ближайшая остановка: Площадь Свободы.\n"
                 "В 5ке.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["fifth"]["latitude"],
            longitude=constants.buildings["fifth"]["longitude"]
        )
    elif "third" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Читальный зал №3*\n\n"
                 "Ближайшие остановки: Толстого и Гоголя.\n"
                 "В 3ке.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["third"]["latitude"],
            longitude=constants.buildings["third"]["longitude"]
        )
    elif "ninth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Читальный зал №9*\n\n"
                 "Ближайшие остановки: Гоголя и Толстого.\n"
                 "В 7ке.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["seventh"]["latitude"],
            longitude=constants.buildings["seventh"]["longitude"]
        )
    elif "sci-tech" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Научно-техническая библиотека*\n\n"
                 "Ближайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.\n"
                 "В 8ке.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["eighth"]["latitude"],
            longitude=constants.buildings["eighth"]["longitude"]
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

    if "first" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Первое общежитие*\n\n"
                 "Ближайшая остановка: КАИ.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["first"]["latitude"],
            longitude=constants.dorms["first"]["longitude"]
        )
    elif "second" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Второе общежитие*\n\n"
                 "Ближайшая остановка: КАИ.\n"
                 "Есть столовая.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["second"]["latitude"],
            longitude=constants.dorms["second"]["longitude"]
        )
    elif "third" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Третье общежитие*\n\n"
                 "Ближайшие остановки: Попова, Пионерская, Губкина, ТД Риф Эль.\n"
                 "Есть столовая.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["third"]["latitude"],
            longitude=constants.dorms["third"]["longitude"]
        )
    elif "fourth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Четвёртое общежитие*\n\n"
                 "Ближайшие остановки: Солнышко, Короленко, Октябрьская, Голубятникова.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["fourth"]["latitude"],
            longitude=constants.dorms["fourth"]["longitude"]
        )
    elif "fifth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Пятое общежитие*\n\n"
                 "Ближайшие остановки: Абжалилова, Кооперативный институт, Патриса Лумумбы, парк Горького.\n"
                 "Есть столовая.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["fifth"]["latitude"],
            longitude=constants.dorms["fifth"]["longitude"]
        )
    elif "sixth" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Шестое общежитие*\n\n"
                 "Ближайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["sixth"]["latitude"],
            longitude=constants.dorms["sixth"]["longitude"]
        )
    elif "seventh" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Седьмое общежитие*\n\n"
                 "Ближайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["seventh"]["latitude"],
            longitude=constants.dorms["seventh"]["longitude"]
        )

@bot.message_handler(commands=["settings"])
def settings(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text="Отправь номер своей группы в формате: 1234",
        reply_markup=keyboards.remove_keyboard()
    )

@bot.message_handler(
    func=lambda m:
        True if re.fullmatch("[1-59][1-6][0-9][0-9]", m.text) else False
)
def remember_group_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    student.student.set_group_number(message.text)
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Отправь номер своей зачётки в формате: 123456",
        reply_markup=keyboards.remove_keyboard()
    )

@bot.message_handler(
    func=lambda m:
        True if re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9]", m.text) else False
)
def remember_student_card_number(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

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

@bot.message_handler(
    func=lambda m:
        m.chat.id == secrets.CREATOR and m.text == "What can I do?"
)
def reverseweek(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="*You can:*\n"
             "/reverseweek - to show whether week is even or odd correctly",
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

print("Bot was launched!")
bot.polling()
