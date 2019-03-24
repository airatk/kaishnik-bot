from bot import kaishnik
from bot import students

from bot.constants import CREATOR
from bot.constants import CREATOR_COMMAND

from bot.helpers import save_users
from bot.helpers import reverse_week_in_file

from datetime import datetime

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["creator"]
)
def creator(message):
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=CREATOR_COMMAND,
        parse_mode="Markdown"
    )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["users"]
)
def users(message):
    institutes_stats = [students[user].get_institute() for user in students]
    years_stats = [students[user].get_year() for user in students]
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=(
            "*Institutes*\n"
            "• ИАНТЭ: {}\n"
            "• ФМФ: {}\n"
            "• ИАЭП: {}\n"
            "• ИКТЗИ: {}\n"
            "• КИТ: {}\n"
            "• ИРЭТ: {}\n"
            "• ИЭУСТ: {}\n"
            "\n*Years*\n"
            "• 1: {}\n"
            "• 2: {}\n"
            "• 3: {}\n"
            "• 4: {}\n"
            "• 5: {}\n"
            "• 6: {}\n\n"
            "*{}* #users in total!".format(
                institutes_stats.count("1"),
                institutes_stats.count("2"),
                institutes_stats.count("3"),
                institutes_stats.count("4"),
                institutes_stats.count("КИТ"),
                institutes_stats.count("5"),
                institutes_stats.count("28"),
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
    commands=["clear"]
)
def clear(message):
    is_cleared = False
    
    for user in list(students):
        try:
            kaishnik.send_chat_action(chat_id=user, action="upload_document")
        except:
            is_cleared = True
            
            kaishnik.send_message(
                chat_id=message.chat.id,
                text=(
                    "{first_name} {last_name} (@{user}) stopped using the bot, so was #erased.\n\n"
                    "• Institute: {institute}\n"
                    "• Year: {year}\n"
                    "• Student card number: {student_card_number}\n"
                    "• Chat ID: {chat_id}".format(
                        first_name=kaishnik.get_chat(chat_id=user).first_name,
                        last_name=kaishnik.get_chat(chat_id=user).last_name,
                        user=kaishnik.get_chat(chat_id=user).username,
                        institute=students[user].get_institute(),
                        year=students[user].get_year(),
                        student_card_number=students[user].get_student_card_number(),
                        chat_id=user
                    )
                ),
                parse_mode="Markdown"
            )
            
            del students[user]

    save_users(students)
    
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
    
    save_users(students)
    
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
        except:
            kaishnik.send_message(
                chat_id=message.chat.id,
                text="Inactive user occured! /clear?"
            )

@kaishnik.message_handler(
    func=lambda message:
        message.chat.id == CREATOR,
    commands=["reverseweek"]
)
def reverseweek(message):
    reverse_week_in_file()
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Reversed!"
    )
