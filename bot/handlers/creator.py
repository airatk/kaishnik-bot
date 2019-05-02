from bot import kbot
from bot import students
from bot import metrics

from bot.student import Student

from bot.constants import CREATOR
from bot.constants import TOKEN

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
                "\t\t\t\[ number:{} ]\[ group:{} ]\n"
                "\t\t\t\[ name:{} ]\n"
            "}\n"
            "\n*data*\n"                ### data
            "/clear\n"
            "/erase { :chat ID: }\n"
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
    institutes_stats = [ students[user].institute for user in students ]
    years_stats = [ students[user].year for user in students ]
    
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
    if "drop" in message.text:
        metrics.zerofy()
    
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
    def send():
        kbot.send_message(
            chat_id=message.chat.id,
            text=(
                "{firstname} {lastname} @{user}\n"
                "chat id {chatid}\n\n"
                "• Institute: {institute}\n"
                "• Year: {year}\n"
                "• Group: {group_number}\n"
                "• Name: {name}\n"
                "• Student card number: {card}\n\n"
                "• Number of notes: {notes_number}\n"
                "• Number of edited classes: {edited_classes_number}\n"
                "• Number of fellow students: {fellow_students_number}\n"
                "\n#data".format(
                    firstname=kbot.get_chat(chat_id=user).first_name,
                    lastname=kbot.get_chat(chat_id=user).last_name,
                    user=kbot.get_chat(chat_id=user).username,
                    chatid=user,
                    institute=students[user].institute,
                    year=students[user].year,
                    group_number=students[user].group_number,
                    name=students[user].name,
                    card=students[user].student_card_number,
                    notes_number=len(students[user].notes),
                    edited_classes_number=len(students[user].edited_subjects),
                    fellow_students_number=len(students[user].names)
                )
            )
        )
    
    text = message.text.replace("/data ", "")
    counter = 0
    
    # Reversing list of students to show new users first
    if "number" in text:
        try:
            asked_users_number = int(text.replace("number:", ""))
        except ValueError:
            asked_users_number = 0
        
        for user in list(students)[::-1][:asked_users_number]:
            send()
            counter += 1
    elif "group" in text:
        asked_users_group = text.replace("group:", "")
        
        for user in list(students)[::-1]:
            if students[user].group_number == asked_users_group:
                send()
                counter += 1
    elif "name" in text:
        asked_users_name = text.replace("name:", "")
        
        for user in list(students)[::-1]:
            if students[user].name is not None and asked_users_name in students[user].name:
                send()
                counter += 1
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Incorrect options!"
        )
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="*{shown}/{total}* users were shown!".format(shown=counter, total=len(students)),
        parse_mode="Markdown"
    )


@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["clear"]
)
def clear(message):
    is_cleared = False
    
    for user in list(students):
        try:
            kbot.get_chat(chat_id=user)
        except:
            is_launched = False
        else:
            is_launched = True
        
        try:
            kbot.send_chat_action(chat_id=user, action="typing")
            
            if not is_launched:
                raise Exception()
            
            if students[user].is_not_set_up():
                raise Exception()
        except Exception:
            is_cleared = True
            
            kbot.send_message(
                chat_id=message.chat.id,
                text=(
                    "{first_name} {last_name} @{user}\n"
                    "chat id {chat_id}\n\n"
                    "• Institute: {institute}\n"
                    "• Year: {year}\n"
                    "• Group: {group_number}\n"
                    "• Name: {name}\n"
                    "• Student card number: {student_card_number}\n"
                    "\n#erased".format(
                        first_name=kbot.get_chat(chat_id=user).first_name if is_launched else "None",
                        last_name=kbot.get_chat(chat_id=user).last_name if is_launched else "None",
                        user=kbot.get_chat(chat_id=user).username if is_launched else "None",
                        chat_id=user,
                        institute=students[user].institute,
                        year=students[user].year,
                        group_number=students[user].group_number,
                        name=students[user].name,
                        student_card_number=students[user].student_card_number
                    )
                )
            )
            
            del students[user]

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
    try:
        chat_id = int(message.text.replace("/erase ", ""))
    except ValueError:
        chat_id = 0
    
    try:
        del students[chat_id]
    except KeyError:
        kbot.send_message(
            chat_id=message.chat.id,
            text="There is *{}* chat ID!".format(chat_id),
            parse_mode="Markdown"
        )
    else:
        save_to(filename="data/users", object=students)
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="{chat_id} was #erased!".format(chat_id=chat_id)
        )

@kbot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=["drop"]
)
def drop(message):
    if "all" not in message.text:
        kbot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to drop all users' data, type */drop all*",
            parse_mode="Markdown"
        )
    else:
        for user in list(students):
            kbot.send_message(
                chat_id=user,
                text="Текущие настройки сброшены, нужно обновить данные. Отправь /settings",
                disable_notification=True
            )
            
            if students[user].notes != []:
                kbot.send_message(
                    chat_id=user,
                    text="Держи свои заметки, чтобы ничего не потерялось:",
                    disable_notification=True
                )
                
                for note in students[user].notes:
                    kbot.send_message(
                        chat_id=user,
                        text=note,
                        parse_mode="Markdown",
                        disable_notification=True
                    )
        
            students[user] = Student()
        
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
    broadcast_message = message.text[11:]
    
    if broadcast_message == "":
        kbot.send_message(
            chat_id=message.chat.id,
            text="No broadcast message was found! It's supposed to be right after the */broadcast* command.",
            parse_mode="Markdown"
        )
    else:
        for user in students:
            kbot.send_message(
                chat_id=user,
                text=(
                    "*Телеграмма от разработчика*\n"
                    "#broadcast\n\n"
                    "{broadcast_message}\n\n"
                    "Написать разработчику: @airatk".format(broadcast_message=broadcast_message)
                ),
                parse_mode="Markdown",
                disable_web_page_preview=True
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
        save_to(filename="data/is_week_reversed", object=False if load_from(filename="data/is_week_reversed") else True)
        
        kbot.send_message(
            chat_id=message.chat.id,
            text="Week type was reversed!"
        )
