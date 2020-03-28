from aiogram.types import Message
from aiogram.types import Chat
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.exceptions import Unauthorized

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.helpers import parse_creator_query
from bot.commands.creator.utilities.helpers import collect_ids
from bot.commands.creator.utilities.helpers import get_user_data
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import USERS_STATS
from bot.commands.creator.utilities.constants import COMMAND_REQUESTS_STATS
from bot.commands.creator.utilities.types import Option

from bot.shared.api.constants import INSTITUTES
from bot.shared.api.student import Student
from bot.shared.commands import Commands

from datetime import datetime


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.USERS.value ]
)
async def users(message: Message):
    institutes_stats: [str] = [ student.institute for student in students.values() ]
    years_stats: [str] = [ student.year for student in students.values() ]
    
    institutes_names: [str] = list(INSTITUTES.values())
    years_names: [str] = [ str(year) for year in range(1, 7) ]  # 6 years maximum
    
    await message.answer(
        text=USERS_STATS.format(
            faculty_1=institutes_names[0], faculty_1_number=institutes_stats.count(institutes_names[0]),
            faculty_2=institutes_names[1], faculty_2_number=institutes_stats.count(institutes_names[1]),
            faculty_3=institutes_names[2], faculty_3_number=institutes_stats.count(institutes_names[2]),
            faculty_4=institutes_names[3][2:-2], faculty_4_number=institutes_stats.count(institutes_names[3]),
            faculty_5=institutes_names[4], faculty_5_number=institutes_stats.count(institutes_names[4]),
            faculty_6=institutes_names[5], faculty_6_number=institutes_stats.count(institutes_names[5]),
            year_1=years_names[0], year_1_number=years_stats.count(years_names[0]),
            year_2=years_names[1], year_2_number=years_stats.count(years_names[1]),
            year_3=years_names[2], year_3_number=years_stats.count(years_names[2]),
            year_4=years_names[3], year_4_number=years_stats.count(years_names[3]),
            year_5=years_names[4], year_5_number=years_stats.count(years_names[4]),
            year_6=years_names[5], year_6_number=years_stats.count(years_names[5]),
            type_1=Student.Type.EXTENDED.value,
            type_1_number=sum(1 for student in students.values() if student.type is Student.Type.EXTENDED),
            type_2=Student.Type.COMPACT.value,
            type_2_number=sum(1 for student in students.values() if student.type is Student.Type.COMPACT),
            type_3=Student.Type.GROUP_CHAT.value,
            type_3_number=sum(1 for student in students.values() if student.type is Student.Type.GROUP_CHAT),
            unsetup_number=sum(1 for student in students.values() if not student.is_setup),
            total=len(students)
        ),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.METRICS.value ]
)
async def metrics_command(message: Message):
    options: {str: str} = parse_creator_query(message.get_args())
    
    if options.get("") == "drop" or metrics.day != datetime.today().isoweekday(): metrics.drop()
    
    await message.answer(
        text=COMMAND_REQUESTS_STATS.format(
            classes_request_number=metrics.classes,
            score_request_number=metrics.score,
            lecturers_request_number=metrics.lecturers,
            notes_request_number=metrics.notes,
            week_request_number=metrics.week,
            exams_request_number=metrics.exams,
            locations_request_number=metrics.locations,
            brs_request_number=metrics.brs,
            edit_request_number=metrics.edit,
            settings_request_number=metrics.settings,
            help_request_number=metrics.help,
            donate_request_number=metrics.donate,
            cancel_request_number=metrics.cancel,
            start_request_number=metrics.start,
            login_request_number=metrics.login,
            unlogin_request_number=metrics.unlogin,
            unknown_nontext_message_request_number=metrics.unknown_nontext_message, unknown_text_message_request_number=metrics.unknown_text_message, unknown_callback_request_number=metrics.unknown_callback,
            no_permissions_number=metrics.no_permissions,
            total_request_number=metrics.sum
        ),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.DATA.value ]
)
async def data(message: Message):
    if message.get_args() == "":
        await message.answer(text="No options were found!")
        return
    
    options: {str: str} = parse_creator_query(message.get_args())
    
    full_users_list: [int] = list(students)[::-1]  # Reversing list of students to show the new users first
    asked_users_list: [int] = []
    inactives_list: [int] = []
    
    progress_bar: str = ""
    
    if Option.IDS.value in options:
        asked_users_list = await collect_ids(query_message=message)
    elif Option.USERNAME.value in options or Option.FIRSTNAME.value in options:
        loading_message = await message.answer(text="Started searching...")
        
        for (index, chat_id) in enumerate(full_users_list):
            progress_bar = await update_progress_bar(
                loading_message=loading_message, current_progress_bar=progress_bar,
                values=full_users_list, index=index
            )
            
            try:
                chat: Chat = await message.bot.get_chat(chat_id=chat_id)
            except (ChatNotFound, Unauthorized):
                await message.answer(text="Troubles getting the {chat_id} chat.".format(chat_id=chat_id))
                continue
            
            does_username_match = Option.USERNAME.value in options and (chat.username is not None and options[Option.USERNAME.value] in chat.username)
            does_firstname_match = Option.FIRSTNAME.value in options and (chat.first_name is not None and options[Option.FIRSTNAME.value] in chat.first_name)
            
            if does_username_match or does_firstname_match: asked_users_list.append(chat_id)
    elif Option.NUMBER.value in options:
        try:
            asked_users_number: int = int(options[Option.NUMBER.value])
        except ValueError:
            asked_users_number: int = 0
        
        asked_users_list = full_users_list[:asked_users_number]
    elif Option.INDEX.value in options:
        try:
            index = int(options[Option.INDEX.value])
            asked_index_user = full_users_list[index]
        except ValueError:
            await message.answer(
                text="*{non_index}* cannot be an index!".format(non_index=options[Option.INDEX.value]),
                parse_mode="markdown"
            )
            return
        except IndexError:
            await message.answer(
                text="*{non_index}* is not currently an index!".format(non_index=options[Option.INDEX.value]),
                parse_mode="markdown"
            )
            return
        else:
            asked_users_list.append(asked_index_user)
    elif Option.NAME.value in options:
        asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].name is not None and options[Option.NAME.value] in students[chat_id].name ]
    elif Option.GROUP.value in options:
        asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].group is not None and options[Option.GROUP.value] in students[chat_id].group ]
    elif Option.YEAR.value in options:
        asked_users_list = [ chat_id for chat_id in full_users_list if students[chat_id].year == options[Option.YEAR.value] ]
    
    progress_bar = ""
    loading_message: Message = await message.answer(text="Started showing...")
    
    for (index, chat_id) in enumerate(asked_users_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=asked_users_list, index=index
        )
        
        try:
            chat: Chat = await message.bot.get_chat(chat_id=chat_id)
        except (ChatNotFound, Unauthorized):
            await message.answer(text="Troubles getting the {chat_id} chat.".format(chat_id=chat_id))
            
            inactives_list.append(chat_id)
        else:
            await message.answer(text=get_user_data(chat=chat, student=students[chat_id], hashtag="data"))
    
    if len(inactives_list) != 0:
        await message.answer(
            text="There is *1* inactive user." if len(inactives_list) == 1 else "There are *{number}* inactive users.".format(number=len(inactives_list)),
            parse_mode="markdown"
        )
    
    if len(asked_users_list) == 0:
        await loading_message.edit_text(text="No user matches the options!")
    else:
        await message.answer(
            text="*{shown}/{total}* users {auxiliary} shown!".format(shown=len(asked_users_list), total=len(students), auxiliary="was" if len(asked_users_list) == 1 else "were"),
            parse_mode="markdown"
        )
