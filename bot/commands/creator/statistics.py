from bot import bot
from bot import students
from bot import metrics

from bot.commands.creator.utilities.helpers import parse_creator_request
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import USERS_STATS
from bot.commands.creator.utilities.constants import COMMAND_REQUESTS_STATS
from bot.commands.creator.utilities.constants import USER_DATA
from bot.commands.creator.utilities.types import DataOption

from bot.shared.api.constants import INSTITUTES
from bot.shared.commands import Commands

from datetime import datetime


@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.USERS.value ]
)
def users(message):
    institutes_stats = [ student.institute for student in students.values() ]
    years_stats = [ student.year for student in students.values() ]
    
    institutes_names = list(INSTITUTES.values())
    years_names = [ str(i) for i in range(1, 7) ]  # 6 years maximum
    
    bot.send_message(
        chat_id=message.chat.id,
        text=USERS_STATS.format(
            faculty_1=institutes_names[0], number_faculty_1=institutes_stats.count(institutes_names[0]),
            faculty_2=institutes_names[1], number_faculty_2=institutes_stats.count(institutes_names[1]),
            faculty_3=institutes_names[2], number_faculty_3=institutes_stats.count(institutes_names[2]),
            faculty_4=institutes_names[3], number_faculty_4=institutes_stats.count(institutes_names[3]),
            faculty_5=institutes_names[4], number_faculty_5=institutes_stats.count(institutes_names[4]),
            faculty_6=institutes_names[5], number_faculty_6=institutes_stats.count(institutes_names[5]),
            year_1=years_names[0], number_year_1=years_stats.count(years_names[0]),
            year_2=years_names[1], number_year_2=years_stats.count(years_names[1]),
            year_3=years_names[2], number_year_3=years_stats.count(years_names[2]),
            year_4=years_names[3], number_year_4=years_stats.count(years_names[3]),
            year_5=years_names[4], number_year_5=years_stats.count(years_names[4]),
            year_6=years_names[5], number_year_6=years_stats.count(years_names[5]),
            number_group_only=sum(1 for student in students.values() if not student.is_full),
            number_unsetup=sum(1 for student in students.values() if not student.is_setup),
            total=len(students)
        ),
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.METRICS.value ]
)
def get_metrics(message):
    (option, _) = parse_creator_request(message.text)
    
    if option == "drop" or metrics.day != datetime.today().isoweekday():
        metrics.drop()
    
    bot.send_message(
        chat_id=message.chat.id,
        text=COMMAND_REQUESTS_STATS.format(
            classes_request_number=metrics.classes,
            score_request_number=metrics.score,
            lecturers_request_number=metrics.lecturers,
            week_request_number=metrics.week,
            notes_request_number=metrics.notes,
            exams_request_number=metrics.exams,
            locations_request_number=metrics.locations,
            card_request_number=metrics.card,
            brs_request_number=metrics.brs,
            me_request_number=metrics.me,
            cancel_request_number=metrics.cancel,
            start_request_number=metrics.start,
            login_request_number=metrics.login,
            unlogin_request_number=metrics.unlogin,
            edit_request_number=metrics.edit,
            help_request_number=metrics.help,
            donate_request_number=metrics.donate,
            unknown_request_number=metrics.unknown,
            total_request_number=metrics.sum
        ),
        parse_mode="Markdown"
    )

@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DATA.value ]
)
def data(message):
    (option, option_data) = parse_creator_request(message.text)
    
    full_users_list = list(students)[::-1]  # Reversing list of students to show new users first
    asked_users_list = []

    try:
        if option == DataOption.ALL.value:
            asked_users_list = full_users_list
        elif option == DataOption.UNLOGIN.value:
            asked_users_list = [ chat_id for chat_id in full_users_list if not students[chat_id].is_setup ]
        elif option == DataOption.ME.value:
            asked_users_list = [ message.chat.id ]
        elif option == DataOption.NUMBER.value:
            asked_users_list = full_users_list[:int(option_data)]
        elif option == DataOption.INDEX.value:
            asked_users_list.append(full_users_list[int(option_data)])
        elif option == DataOption.NAME.value:
            asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].name is not None and message.text.split(":")[1] in students[chat_id].name ]
        elif option == DataOption.GROUP.value:
            asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].group is not None and option_data in students[chat_id].group ]
        elif option == DataOption.YEAR.value:
            asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].year == option_data ]
        else:
            raise
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text="Incorrect option!"
        )
        return
    
    for chat_id in asked_users_list:
        try:
            chat = bot.get_chat(chat_id=chat_id)
        except Exception:
            bot.send_message(
                chat_id=message.chat.id,
                text="{} is inactive! /clear?".format(chat_id)
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=USER_DATA.format(
                    firstname=chat.first_name, lastname=chat.last_name, username=chat.username,
                    chat_id=chat_id,
                    institute=students[chat_id].institute,
                    year=students[chat_id].year,
                    group_number=students[chat_id].group,
                    name=students[chat_id].name,
                    card=students[chat_id].card,
                    notes_number=len(students[chat_id].notes),
                    edited_classes_number=len(students[chat_id].edited_subjects),
                    fellow_students_number=len(students[chat_id].names),
                    is_full=students[chat_id].is_full,
                    guard_text=students[chat_id].guard.text,
                    is_guard_message_none=students[chat_id].guard.message is None,
                    hashtag="data"
                )
            )

    bot.send_message(
        chat_id=message.chat.id,
        text="*{shown}/{total}* users were shown!".format(shown=len(asked_users_list), total=len(students)),
        parse_mode="Markdown"
    )
