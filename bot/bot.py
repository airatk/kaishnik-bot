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
    
    for weekday in constants.week.keys():
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

    if "1" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["1"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["1"]["latitude"],
            longitude=constants.buildings["1"]["longitude"]
        )
    elif "2" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["2"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["2"]["latitude"],
            longitude=constants.buildings["2"]["longitude"]
        )
    elif "3" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["3"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["3"]["latitude"],
            longitude=constants.buildings["3"]["longitude"]
        )
    elif "4" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["4"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["4"]["latitude"],
            longitude=constants.buildings["4"]["longitude"]
        )
    elif "5" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["5"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["5"]["latitude"],
            longitude=constants.buildings["5"]["longitude"]
        )
    elif "6" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["6"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["6"]["latitude"],
            longitude=constants.buildings["6"]["longitude"]
        )
    elif "7" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["7"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["7"]["latitude"],
            longitude=constants.buildings["7"]["longitude"]
        )
    elif "8" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["8"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["8"]["latitude"],
            longitude=constants.buildings["8"]["longitude"]
        )
    elif "СК Олимп" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.buildings["СК Олимп"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["СК Олимп"]["latitude"],
            longitude=constants.buildings["СК Олимп"]["longitude"]
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

    if "1" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.libraries["1"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["1"]["latitude"],
            longitude=constants.buildings["1"]["longitude"]
        )
    elif "2" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.libraries["2"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["5"]["latitude"],
            longitude=constants.buildings["5"]["longitude"]
        )
    elif "3" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.libraries["3"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["3"]["latitude"],
            longitude=constants.buildings["3"]["longitude"]
        )
    elif "9" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.libraries["9"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["7"]["latitude"],
            longitude=constants.buildings["7"]["longitude"]
        )
    elif "научно-техническая" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.libraries["научно-техническая"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.buildings["8"]["latitude"],
            longitude=constants.buildings["8"]["longitude"]
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

    if "1" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["1"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["1"]["latitude"],
            longitude=constants.dorms["1"]["longitude"]
        )
    elif "2" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["2"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["2"]["latitude"],
            longitude=constants.dorms["2"]["longitude"]
        )
    elif "3" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["3"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["3"]["latitude"],
            longitude=constants.dorms["3"]["longitude"]
        )
    elif "4" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["4"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["4"]["latitude"],
            longitude=constants.dorms["4"]["longitude"]
        )
    elif "5" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["5"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["5"]["latitude"],
            longitude=constants.dorms["5"]["longitude"]
        )
    elif "6" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["6"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["6"]["latitude"],
            longitude=constants.dorms["6"]["longitude"]
        )
    elif "7" in callback.data:
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=constants.dorms["7"]["description"],
            parse_mode="Markdown"
        )
        bot.send_location(
            chat_id=callback.message.chat.id,
            latitude=constants.dorms["7"]["latitude"],
            longitude=constants.dorms["7"]["longitude"]
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
