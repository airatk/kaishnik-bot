import telebot
import secrets
import constants
import keyboards
import helpers
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
        text=constants.replies_to_unknown_command[0], # Coincidencially this string is on replies_to_unknown_command list :)
        parse_mode="Markdown"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Но прежде настрой меня на общение с тобой" + constants.emoji["smirking"],
        reply_markup=keyboards.settings_entry()
    )

@bot.message_handler(commands=["classes"])
def classes(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    pass

@bot.message_handler(commands=["exams"])
def exams(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    pass

@bot.message_handler(commands=["week"])
def week(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    bot.send_message(
        chat_id=message.chat.id,
        text=helpers.get_week(is_reverse=True)
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

@bot.callback_query_handler(func=lambda callback: callback.data == "buildings")
def b_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 8 учебных зданий и 1 спортивный комплекс:",
        reply_markup=keyboards.buildings_dailer()
    )

@bot.callback_query_handler(func=lambda callback: True if "b_s" in callback.data else False)
def send_building(callback):
    if "first" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Первый дом*\n\nБлижайшая остановка: КАИ.\nЕсть буфет и читальный зал №1.",
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
            text="*2ка*\n\nБлижайшие остановки: Четаева, Чистопольская, Амирхана, СК Олимп.\nЕсть буфет.",
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
            text="*3ка*\n\nБлижайшие остановки: Толстого и Гоголя.\nЕсть буфет и читальный зал №3.",
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
            text="*4ка*\n\nБлижайшие остановки: Толстого и Гоголя.\nНи буфета, ни читального зала - грустно!",
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
            text="*5ка*\n\nБлижайшая остановка: Площадь Свободы.\nЕсть столовая и читальный зал №2.",
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
            text="*6ка*\n\nБлижайшие остановки: Институт, Кошевого, КМПО.\nЕсть буфет.",
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
            text="*7ка*\n\nБлижайшие остановки: Гоголя и Толстого.\nЕсть буфет и читальный зал №9.",
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
            text="*8ка*\n\nБлижайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.\nЕсть буфет и научно-техническая библиотека.",
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
            text="*СК Олимп*\n\nБлижайшие остановки: СК Олимп, Чистопольская, Четаева, Амирхана.\nНа самом деле, у Олимпа два здания: основное и здание бассейна, а ещё есть стадион.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["olymp"]["latitude"],
            longitude=constants.buildings["olymp"]["longitude"]
        )

@bot.callback_query_handler(func=lambda callback: callback.data == "libraries")
def b_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 5 библиотек:",
        reply_markup=keyboards.libraries_dailer()
    )

@bot.callback_query_handler(func=lambda callback: True if "l_s" in callback.data else False)
def send_library(callback):
    if "first" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Читальный зал №1*\n\nБлижайшая остановка: КАИ.\nВ первом доме.",
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
            text="*Читальный зал №2*\n\nБлижайшая остановка: Площадь Свободы.\nВ 5ке.",
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
            text="*Читальный зал №3*\n\nБлижайшие остановки: Толстого и Гоголя.\nВ 3ке.",
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
            text="*Читальный зал №9*\n\nБлижайшие остановки: Гоголя и Толстого.\nВ 7ке.",
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
            text="*Научно-техническая библиотека*\n\nБлижайшие остановки: Чистопольская, Четаева, СК Олимп, Амирхана.\nВ 8ке.",
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["eighth"]["latitude"],
            longitude=constants.buildings["eighth"]["longitude"]
        )

@bot.callback_query_handler(func=lambda callback: callback.data == "dorms")
def d_s(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 7 общежитий:",
        reply_markup=keyboards.dorms_dailer()
    )

@bot.callback_query_handler(func=lambda callback: True if "d_s" in callback.data else False)
def send_dorm(callback):
    if "first" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*Первое общежитие*\n\nБлижайшая остановка: КАИ.",
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
            text="*Второе общежитие*\n\nБлижайшая остановка: КАИ.\nЕсть столовая.",
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
            text="*Третье общежитие*\n\nБлижайшие остановки: Попова, Пионерская, Губкина, ТД Риф Эль.\nЕсть столовая.",
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
            text="*Четвёртое общежитие*\n\nБлижайшие остановки: Солнышко, Короленко, Октябрьская, Голубятникова.",
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
            text="*Пятое общежитие*\n\nБлижайшие остановки: Абжалилова, Кооперативный институт, Патриса Лумумбы, парк Горького.\nЕсть столовая.",
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
            text="*Шестое общежитие*\n\nБлижайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
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
            text="*Седьмое общежитие*\n\nБлижайшие остановки: Вишневского, Товарищеская, Достоевского, Калинина.",
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

    pass

@bot.message_handler(func=lambda m: m.text[0] == "/")
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
        text=random.choice(constants.replies_to_unknown_command + constants.replies_to_unknown_message),
        parse_mode="Markdown"
    )

print("Bot was launched!")
bot.polling()
