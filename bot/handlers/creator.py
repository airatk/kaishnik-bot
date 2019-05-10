from bot import kbot
from bot import students
from bot import metrics

from bot.student import Student

from bot.constants import CREATOR
from bot.constants import TOKEN

from bot.keyboards.start import make_setup

from bot.helpers import save_to
from bot.helpers import load_from

from datetime import datetime


@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["creator"]
)
def creator(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "*Control panel*\n"         # {} - required, [] - optional
            "_creator access only_\n"
            "\n*stats*\n"               ### stats
            "/users\n"
            "/metrics \[ drop ]\n"
            "/data {\n"
                "\t\t\t\[ number:{} ]\[ name:{} ]\n"
                "\t\t\t\[ group:{} ]\[ year:{} ]\n"
            "}\n"
            "\n*data*\n"                ### data
            "/clear\n"
            "/erase {\n"
                "\t\t\t\[ all ]\[ :chat ID 1:, … ]\n"
            "}\n"
            "/drop { all }\n"
            "\n*others*\n"              ### others
            "/broadcast { :message: }\n"
            "/reverse { week }\n"
            "\n*hashtags*\n"            ### hashtags
            "# users\n"
            "# metrics\n"
            "# data\n"
            "# erased\n"
            "# broadcast\n"
            "# dropped"
        ),
        parse_mode="Markdown"
    )


@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["users"]
)
def users(message):
    institutes_stats = [ student.institute for _, student in students.items() ]
    years_stats = [ student.year for _, student in students.items() ]
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "*Users*\n"
            "_stats of_ #users\n"
            "\n*institutes*\n"          ### institutes
            "• ИАНТЭ: {}\n"
            "• ФМФ: {}\n"
            "• ИАЭП: {}\n"
            "• ИКТЗИ: {}\n"
            "• КИТ: {}\n"
            "• ИРЭТ: {}\n"
            "• ИЭУСТ: {}\n"
            "\n*years*\n"               ### years
            "• 1: {}\n"
            "• 2: {}\n"
            "• 3: {}\n"
            "• 4: {}\n"
            "• 5: {}\n"
            "• 6: {}\n\n"
            "*{}* users in total!".format(
                institutes_stats.count("ИАНТЭ"),
                institutes_stats.count("ФМФ"),
                institutes_stats.count("ИАЭП"),
                institutes_stats.count("♥ ИКТЗИ ♥"),
                institutes_stats.count("КИТ"),
                institutes_stats.count("ИРЭТ"),
                institutes_stats.count("ИЭУСТ"),
                years_stats.count("1"),
                years_stats.count("2"),
                years_stats.count("3"),
                years_stats.count("4"),
                years_stats.count("5"),
                years_stats.count("6"),
                len(students)
            )
        ),
        parse_mode="Markdown"
    )

@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["metrics"]
)
def get_metrics(message):
    if "drop" in message.text: metrics.zerofy()
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "*Metrics*\n"
            "_daily_ #metrics\n"
            "\n*usage*\n"               ### usage
            "/classes: {}\n"
            "/score: {}\n"
            "/lecturers: {}\n"
            "/week: {}\n"
            "/notes: {}\n"
            "/exams: {}\n"
            "/locations: {}\n"
            "/card: {}\n"
            "/brs: {}\n"
            "\n*setup*\n"               ### setup
            "/start: {}\n"
            "/settings: {}\n"
            "unsetup: {}\n"
            "\n*other*\n"               ### other
            "/edit: {}\n"
            "/help: {}\n"
            "/donate: {}\n"
            "unknown: {}\n"
            "\n*{}* requests in total!".format(
                metrics.classes,
                metrics.score,
                metrics.lecturers,
                metrics.week,
                metrics.notes,
                metrics.exams,
                metrics.locations,
                metrics.card,
                metrics.brs,
                metrics.start,
                metrics.settings,
                metrics.unsetup,
                metrics.edit,
                metrics.help,
                metrics.donate,
                metrics.unknown,
                metrics.sum
            )
        ),
        parse_mode="Markdown"
    )

@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["data"]
)
def data(message):
    option = message.text.replace("/data ", "")
    is_correct = True
    
    asked_users_list = []
    full_users_list = list(students)[::-1]  # Reversing list of students to show new users first
    
    if option.startswith("number:"):
        try: asked_users_number = int(option.replace("number:", ""))
        except ValueError: asked_users_number = 0
        
        asked_users_list = full_users_list[:asked_users_number]
    elif option.startswith("name:"):
        asked_users_name = option.replace("name:", "")
        
        asked_users_list = [
            chat_id for chat_id in full_users_list if (
                students[chat_id].name is not None and asked_users_name in students[chat_id].name
            )
        ]
    elif option.startswith("group:"):
        asked_users_group = option.replace("group:", "")
        
        asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].group_number == asked_users_group ]
    elif option.startswith("year:"):
        asked_users_year = option.replace("year:", "")
        
        asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].year == asked_users_year ]
    else:
        is_correct = False
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="Incorrect options!"
        )
    
    if is_correct:
        for chat_id in asked_users_list:
            chat = kbot.get_chat(chat_id=chat_id)
            
            kbot.send_message(
                chat_id=message.chat.id,
                text=(
                    "{firstname} {lastname} @{username}\n"
                    "chat id {chat_id}\n\n"
                    "• Institute: {institute}\n"
                    "• Year: {year}\n"
                    "• Group: {group_number}\n"
                    "• Name: {name}\n"
                    "• Student card number: {card}\n\n"
                    "• Number of notes: {notes_number}\n"
                    "• Number of edited classes: {edited_classes_number}\n"
                    "• Number of fellow students: {fellow_students_number}\n"
                    "\n#data".format(
                        firstname=chat.first_name,
                        lastname=chat.last_name,
                        username=chat.username,
                        chat_id=chat_id,
                        institute=students[chat_id].institute,
                        year=students[chat_id].year,
                        group_number=students[chat_id].group_number,
                        name=students[chat_id].name,
                        card=students[chat_id].student_card_number,
                        notes_number=len(students[chat_id].notes),
                        edited_classes_number=len(students[chat_id].edited_subjects),
                        fellow_students_number=len(students[chat_id].names)
                    )
                )
            )
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="*{shown}/{total}* users were shown!".format(shown=len(asked_users_list), total=len(students)),
            parse_mode="Markdown"
        )


@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["clear"]
)
def clear(message):
    is_cleared = False
    
    for chat_id in list(students):
        try: kbot.get_chat(chat_id=chat_id)
        except: is_launched = False
        else: is_launched = True
        
        try:
            kbot.send_chat_action(chat_id=chat_id, action="typing")
            
            if not is_launched: raise Exception()
        except Exception:
            is_cleared = True
            
            kbot.send_message(
                chat_id=message.chat.id,
                text=(
                    "{first_name} {last_name} @{username}\n"
                    "chat id {chat_id}\n\n"
                    "• Institute: {institute}\n"
                    "• Year: {year}\n"
                    "• Group: {group_number}\n"
                    "• Name: {name}\n"
                    "• Student card number: {student_card_number}\n"
                    "\n#erased".format(
                        first_name=kbot.get_chat(chat_id=chat_id).first_name if is_launched else "Not launched to get",
                        last_name=kbot.get_chat(chat_id=chat_id).last_name if is_launched else "",
                        username=kbot.get_chat(chat_id=chat_id).username if is_launched else "None",
                        chat_id=chat_id,
                        institute=students[chat_id].institute,
                        year=students[chat_id].year,
                        group_number=students[chat_id].group_number,
                        name=students[chat_id].name,
                        student_card_number=students[chat_id].student_card_number
                    )
                )
            )
            
            del students[chat_id]

    save_to(filename="data/users", object=students)
    
    if is_cleared:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Cleared!"
        )
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="No one has been cleared!"
        )

@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["erase"]
)
def erase(message):
    to_erase = message.text.replace("/erase ", "")
    
    if to_erase == "/erase":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Incorrect options!"
        )
    elif to_erase == "all":
        for chat_id in list(students): del students[chat_id]
        save_to(filename="data/users", object=students)
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="All users were #erased!"
        )
    elif to_erase == "me":
        if message.chat.id in students:
            del students[message.chat.id]
            save_to(filename="data/users", object=students)
            
            kbot.send_message(
                chat_id=message.chat.id,
                text="You, {}, was #erased!".format(message.chat.id)
            )
        else:
            kbot.send_message(
                chat_id=message.chat.id,
                text="There is no {} chat ID!".format(message.chat.id),
            )
    else:
        for chat_id in to_erase.split():
            try:
                del students[int(chat_id)]
            except Exception:
                kbot.send_message(
                    chat_id=message.chat.id,
                    text="There is no {} chat ID!".format(chat_id)
                )
            else:
                kbot.send_message(
                    chat_id=message.chat.id,
                    text="{} was #erased!".format(chat_id)
                )

        save_to(filename="data/users", object=students)

@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["drop"]
)
def drop(message):
    if message.text.replace("/drop ", "") != "all":
        kbot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to drop all users' data, type */drop all*",
            parse_mode="Markdown"
        )
    else:
        for chat_id in list(students):
            if students[chat_id].notes != []:
                for note in students[chat_id].notes:
                    kbot.send_message(
                        chat_id=chat_id,
                        text=note,
                        parse_mode="Markdown",
                        disable_notification=True
                    )

                kbot.send_message(
                    chat_id=chat_id,
                    text="Твои заметки, чтобы ничего не потерялось.",
                    disable_notification=True
                )
            
            students[chat_id] = Student()
            
            students[message.chat.id].previous_message = "/start"  # Gate System (GS)
        
            kbot.send_message(
                chat_id=chat_id,
                text="Текущие настройки сброшены.",
                disable_notification=True
            )
            kbot.send_message(
                chat_id=chat_id,
                text="Обнови данные:",
                reply_markup=make_setup(),
                disable_notification=True
            )
        
        save_to(filename="data/users", object=students)

        kbot.send_message(
            chat_id=message.chat.id,
            text="All data was #dropped!"
        )


@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["broadcast"]
)
def broadcast(message):
    broadcast_message = message.text.replace("/broadcast ", "")
    
    if broadcast_message == "/broadcast":
        kbot.send_message(
            chat_id=message.chat.id,
            text="No broadcast message was found! It's supposed to be right after the */broadcast* command.",
            parse_mode="Markdown"
        )
    else:
        for chat_id in students:
            try:
                kbot.send_message(
                    chat_id=chat_id,
                    text=(
                        "*Телеграмма от разработчика*\n"
                        "#broadcast\n\n"
                        "{}\n\n"
                        "Написать разработчику: @airatk".format(broadcast_message)
                    ),
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
            except Exception:
                kbot.send_message(
                    chat_id=message.chat.id,
                    text="Inactive user occured! /clear?"
                )
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="Done! Sent to each & every user."
        )

@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["reverse"]
)
def reverse(message):
    if "week" not in message.text:
        kbot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to reverse type of a week, type */reverse week*",
            parse_mode="Markdown"
        )
    else:
        save_to(filename="data/is_week_reversed", object=not load_from(filename="data/is_week_reversed"))
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="Week type was reversed!"
        )
