from bot import kaishnik
from bot import students
from bot import metrics

from bot.constants import CREATOR

from bot.helpers import save_to
from bot.helpers import load_from

from datetime import datetime

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["creator"]
)
def creator(message):
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=(
            "*Creator's\ncontrol panel*\n"
            "\n*safe*\n"                ### safe
            "/users\n"
            "/metrics _drop_\n"
            "/data\n"
            "/clear\n"
            "\n*unsafe*\n"              ### unsafe
            "/ drop\n"
            "/ broadcast _text_\n"
            "/ reverse\n"
            "\n*hashtags*\n"            ### hashtags
            "#users\n"
            "#metrics\n"
            "#data\n"
            "#erased\n"
            "#dropped\n"
            "#broadcast\n"
            "#update"  # For update notifications, not associated with any command unlike other hashtags
        ),
        parse_mode="Markdown"
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["users"]
)
def users(message):
    institutes_stats = [ students[user].institute for user in students ]
    years_stats = [ students[user].year for user in students ]
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=(
            "*Users*\n"
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
            "*{}* #users in total!".format(
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

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["metrics"]
)
def get_metrics(message):
    if "drop" in message.text:
        metrics.zerofy()
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=(
            "*Metrics*\n"
            "_daily_ #metrics\n"
            "\n*usage*\n"               ### usage
            "/classes: {}\n"
            "/score: {}\n"
            "/lecturers: {}\n"
            "/week: {}\n"
            "/exams: {}\n"
            "/locations: {}\n"
            "/card: {}\n"
            "/brs: {}\n"
            "\n*setup*\n"               ### setup
            "/start: {}\n"
            "/settings: {}\n"
            "unsetup: {}\n"
            "\n*other*\n"               ### other
            "unknown: {}\n"
            "\n*{}* requests in total!".format(
                metrics.classes,
                metrics.score,
                metrics.lecturers,
                metrics.week,
                metrics.exams,
                metrics.locations,
                metrics.card,
                metrics.brs,
                metrics.start,
                metrics.settings,
                metrics.unsetup,
                metrics.unknown,
                metrics.sum
            )
        ),
        parse_mode="Markdown"
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["data"]
)
def data(message):
    for user in students:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text=(
                "*{first_name} {last_name}* @{user}\n"
                "_chat id {chat_id}_\n\n"
                "• *Institute:* {institute}\n"
                "• *Year:* {year}\n"
                "• *Group:* {group_number}\n"
                "• *Name:* {name}\n"
                "• *Student card number:* {student_card_number}\n"
                "\n#data".format(
                    first_name=kaishnik.get_chat(chat_id=user).first_name,
                    last_name=kaishnik.get_chat(chat_id=user).last_name,
                    user=kaishnik.get_chat(chat_id=user).username,
                    chat_id=user,
                    institute=students[user].institute,
                    year=students[user].year,
                    group_number=students[user].group_number,
                    name=students[user].name,
                    student_card_number=students[user].student_card_number
                )
            ),
            parse_mode="Markdown"
        )

    kaishnik.send_message(
        chat_id=message.chat.id,
        text="*{}* users in total!".format(len(students)),
        parse_mode="Markdown"
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["clear"]
)
def clear(message):
    is_cleared = False
    
    for user in list(students):
        try:
            kaishnik.send_chat_action(chat_id=user, action="upload_document")
        except Exception:
            is_cleared = True
            
            kaishnik.send_message(
                chat_id=message.chat.id,
                text=(
                    "*{first_name} {last_name}* @{user}\n"
                    "_chat id {chat_id}_\n\n"
                    "• *Institute:* {institute}\n"
                    "• *Year:* {year}\n"
                    "• *Group:* {group_number}\n"
                    "• *Name:* {name}\n"
                    "• *Student card number:* {student_card_number}\n"
                    "\nStopped using the bot, so was #erased.".format(
                        first_name=kaishnik.get_chat(chat_id=user).first_name,
                        last_name=kaishnik.get_chat(chat_id=user).last_name,
                        user=kaishnik.get_chat(chat_id=user).username,
                        chat_id=user,
                        institute=students[user].institute,
                        year=students[user].year,
                        group_number=students[user].group_number,
                        name=students[user].name,
                        student_card_number=students[user].student_card_number
                    )
                ),
                parse_mode="Markdown"
            )
            
            del students[user]

    save_to(filename="data/users", object=students)
    
    if is_cleared:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Cleared!"
        )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="No one has stopped using the bot!"
        )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["drop"]
)
def drop(message):
    for user in list(students):
        del students[user]
    
    save_to(filename="data/users", object=students)
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="All data was #dropped!"
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["broadcast"]
)
def broadcast(message):
    for user in students:
        try:
            kaishnik.send_message(
                chat_id=user,
                text=(
                    "*Телеграмма от разработчика*\n"
                    "#broadcast\n\n"
                    "{}"
                    "\n\nНаписать разработчику: @airatk".format(message.text[11:])
                ),
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Inactive user occured! /clear?"
            )

    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Done! Sent to each & every user."
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["reverse"]
)
def reverse(message):
    if load_from(filename="data/is_week_reversed"):
        save_to(filename="data/is_week_reversed", object=False)
    else:
        save_to(filename="data/is_week_reversed", object=True)
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Week type was reversed!"
    )
