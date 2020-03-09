from aiogram.types import Chat
from aiogram.types import Message
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.exceptions import Unauthorized

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.creator.utilities.helpers import get_user_data
from bot.commands.creator.utilities.helpers import parse_creator_query
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import USERS_STATS
from bot.commands.creator.utilities.constants import COMMAND_REQUESTS_STATS
from bot.commands.creator.utilities.types import DataOption
from bot.commands.creator.utilities.types import Suboption

from bot.shared.api.constants import INSTITUTES
from bot.shared.commands import Commands

from datetime import datetime


@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.USERS.value ]
)
async def users(message: Message):
    institutes_stats: [str] = [ student.institute for student in students.values() ]
    years_stats: [str] = [ student.year for student in students.values() ]
    
    institutes_names: [str] = list(INSTITUTES.values())
    years_names: [str] = [ str(year) for year in range(1, 7) ]  # 6 years maximum
    
    await message.answer(
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
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
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
            week_request_number=metrics.week,
            notes_request_number=metrics.notes,
            exams_request_number=metrics.exams,
            locations_request_number=metrics.locations,
            card_request_number=metrics.card,
            brs_request_number=metrics.brs,
            cancel_request_number=metrics.cancel,
            start_request_number=metrics.start,
            login_request_number=metrics.login,
            unlogin_request_number=metrics.unlogin,
            settings_request_number=metrics.settings,
            edit_request_number=metrics.edit,
            help_request_number=metrics.help,
            donate_request_number=metrics.donate,
            unknown_request_number=metrics.unknown,
            total_request_number=metrics.sum
        ),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DATA.value ]
)
async def data(message: Message):
    async def collect_asked_users() -> [int]:
        options: {str: str} = parse_creator_query(message.get_args())
        
        full_users_list: [int] = list(students)[::-1]  # Reversing list of students to show the new users first
        asked_users_list: [int] = []
        
        if DataOption.IDS.value in options:
            if options[DataOption.IDS.value] == Suboption.ALL.value:
                return full_users_list
            
            if options[DataOption.IDS.value] == Suboption.UNLOGIN.value:
                asked_users_list += [ chat_id for chat_id in full_users_list if not students[chat_id].is_setup ]
            
            if options[DataOption.IDS.value] == Suboption.ME.value:
                asked_users_list.append(message.chat.id)
            
            asked_users_list += [ chat_id for chat_id in full_users_list if str(chat_id) in options[DataOption.IDS.value] ]
        
        if DataOption.USERNAME.value in options or DataOption.FIRSTNAME.value in options:
            progress_bar: str = ""
            
            loading_message = await message.answer(text="Started searching...")
            
            for (index, chat_id) in enumerate(full_users_list):
                progress_bar = await update_progress_bar(
                    loading_message=loading_message, current_progress_bar=progress_bar,
                    values=full_users_list, index=index
                )
                
                try:
                    chat: Chat = await message.bot.get_chat(chat_id=chat_id)
                except (ChatNotFound, Unauthorized):
                    continue
                
                does_username_match = DataOption.USERNAME.value in options and (chat.username is not None and options[DataOption.USERNAME.value] in chat.username)
                does_firstname_match = DataOption.FIRSTNAME.value in options and (chat.first_name is not None and options[DataOption.FIRSTNAME.value] in chat.first_name)
                
                if does_username_match or does_firstname_match: asked_users_list.append(chat_id)
        
        if DataOption.NUMBER.value in options:
            try:
                asked_users_number: int = int(options[DataOption.NUMBER.value])
            except ValueError:
                asked_users_number: int = 0
            
            asked_users_list += full_users_list[:asked_users_number]
        
        if DataOption.INDEX.value in options:
            try:
                index = int(options[DataOption.INDEX.value])
                asked_index_user = full_users_list[index]
            except (ValueError, IndexError):
                pass
            else:
                asked_users_list.append(asked_index_user)
        
        if DataOption.NAME.value in options:
            asked_users_list += [ chat_id for chat_id in full_users_list if students[chat_id].name is not None and options[DataOption.NAME.value] in students[chat_id].name ]
        
        if DataOption.GROUP.value in options:
            asked_users_list += [ chat_id for chat_id in full_users_list if students[chat_id].group is not None and options[DataOption.GROUP.value] in students[chat_id].group ]
        
        if DataOption.YEAR.value in options:
            asked_users_list += [ chat_id for chat_id in full_users_list if students[chat_id].year == options[DataOption.YEAR.value] ]
        
        return asked_users_list
    
    asked_users_list: [int] = await collect_asked_users()
    inactives_list: [int] = []
    progress_bar: str = ""
    
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
    
    if len(inactives_list) == 1:
        await message.answer(
            text="There is *1* inactive user.",
            parse_mode="markdown"
        )
    elif len(inactives_list) != 0:
        await message.answer(
            text="There are *{number}* inactive users.".format(number=len(inactives_list)),
            parse_mode="markdown"
        )
    
    if len(asked_users_list) == 0: await loading_message.delete()
    
    await message.answer(
        text="*{shown}/{total}* users were shown!".format(shown=len(asked_users_list), total=len(students)),
        parse_mode="markdown"
    )
