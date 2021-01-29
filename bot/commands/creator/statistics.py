from datetime import datetime
from re import compile

from typing import Any
from typing import Dict
from typing import List
from typing import Callable

from aiogram.types import Message

from bot import dispatcher

from bot.commands.creator.utilities.helpers import parse_creator_query
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.helpers import try_get_chat
from bot.commands.creator.utilities.helpers import show_users_list
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import USERS_STATS
from bot.commands.creator.utilities.constants import MONTH_GRAPH
from bot.commands.creator.utilities.constants import COMMAND_REQUESTS_STATS
from bot.commands.creator.utilities.types import Option
from bot.commands.creator.utilities.types import Value

from bot.models.users import Users
from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents
from bot.models.metrics import Metrics

from bot.utilities.types import Commands
from bot.utilities.calendar.constants import MONTHS_EN


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.USERS.value ]
)
async def users(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text)
    
    if len(options) == 0:
        setup_users: Users = Users.select().where(Users.is_setup == True)
        
        users_stats_filing: Dict[str, str] = {
            "groups": GroupsOfStudents.select().where(GroupsOfStudents.user_id.in_(setup_users)).count(),
            "compact": CompactStudents.select().where(CompactStudents.user_id.in_(setup_users)).count(),
            "extended": ExtendedStudents.select().where(ExtendedStudents.user_id.in_(setup_users)).count(),
            "bb": BBStudents.select().where(BBStudents.user_id.in_(setup_users)).count(),
            "setup": setup_users.count(),
            "unsetup": Users.select().where(Users.is_setup == False).count(),
            "total": Users.select().count()
        }
        
        await message.answer(
            text=USERS_STATS.format(**users_stats_filing),
            parse_mode="markdown"
        )
        return
    
    if Option.MONTH.value in options:
        if not compile("^[0-9][0-9][0-9][0-9]-[0-9][0-9]$").match(options[Option.MONTH.value]):
            await message.answer(
                text=(
                    "Incorrect month format!\n"
                    "It should be the following: `yyyy-mm`"
                ),
                parse_mode="markdown"
            )
            return
        
        month: str = "-".join([ options[Option.MONTH.value], "*" ])
        
        month_metrics: List[Metrics] = Metrics.select().where(Metrics.date.regexp(month))
        graph_values: Dict[str, int] = {}
        
        for day_metrics in month_metrics:
            graph_values[day_metrics.date[5:]] = day_metrics.start
        
        PERIOD: int = 20
        max_requests_number: int = max(graph_values.values()) if len(graph_values.values()) != 0 else 0
        get_bar_length: Callable = lambda requests_number: int(requests_number/max_requests_number * PERIOD)
        
        graph: str = "\n".join(sorted([
            "• {day}: {requests_number:<2} {pluses}".format(
                day=date.split("-")[1],
                requests_number=requests_number,
                pluses="".join([ "+" for _ in range(get_bar_length(requests_number) if get_bar_length(requests_number) > 1 else 1) ])
            ) for (date, requests_number) in graph_values.items()
        ], key=lambda string_date: string_date[2:7], reverse=True))
        
        await message.answer(
            text=MONTH_GRAPH.format(
                month=MONTHS_EN.get(options[Option.MONTH.value].split("-")[1], "Unknown Month"),
                hashtag="users",
                graph=graph if graph != "" else "empty",
                total=sum(graph_values.values()),
                average=round(sum(graph_values.values())/len(graph_values.values()))
            ),
            parse_mode="markdown"
        )
        return
    
    users_ids_list: List[int] = []
    
    groups_list: List[GroupsOfStudents] = []
    compacts_list: List[CompactStudents] = []
    extendeds_list: List[ExtendedStudents] = []
    bbs_list: List[ExtendedStudents] = []
    undefined_users_list: List[Users] = []
    
    loading_message: Message = await message.answer(text="Started searching...")
    progress_bar: str = ""
    
    if options.get(Option.EMPTY.value) == Value.ME.value:
        users_ids_list.append(Users.get(Users.telegram_id == message.chat.id).user_id)
    elif Option.NUMBER.value in options:
        try:
            asked_users_number: int = int(options[Option.NUMBER.value])
        except ValueError:
            asked_users_number: int = 0
        
        users_ids_list = [ user.user_id for user in Users.select().order_by(Users.user_id.desc()).limit(asked_users_number) ]
    elif Option.STATE.value in options:
        if options[Option.STATE.value] == Value.SETUP.value:
            is_setup: bool = True
        elif options[Option.STATE.value] == Value.UNSETUP.value:
            is_setup: bool = False
        else:
            await loading_message.edit_text(text="Wrong state value was given!")
            return
        
        users_ids_list = [ user.user_id for user in Users.select().where(Users.is_setup == is_setup) ]
    elif Option.USER_ID.value in options:
        if not options[Option.USER_ID.value].isdigit():
            await loading_message.edit_text(text="User ID should be an integer!")
            return
        
        user_id: int = int(options[Option.USER_ID.value])
        
        if not Users.select().where(Users.user_id == user_id).exists():
            await loading_message.edit_text(text="Asked user doesn't exist!")
            return
        
        users_ids_list.append(user_id)
    elif Option.USERNAME.value in options or Option.FIRSTNAME.value in options:
        users_list: List[Users] = Users.select()
        
        for (index, user) in enumerate(users_list):
            progress_bar = await update_progress_bar(
                loading_message=loading_message, current_progress_bar=progress_bar,
                values_number=users_list.count(), index=index
            )
            
            (chat, _) = await try_get_chat(chat_id=user.telegram_id)
            
            if chat is None: continue
            
            does_username_match = Option.USERNAME.value in options and (
                chat.username is not None and options[Option.USERNAME.value] in chat.username
            )
            does_firstname_match = Option.FIRSTNAME.value in options and (
                chat.first_name is not None and options[Option.FIRSTNAME.value] in chat.first_name
            )
            
            if does_username_match or does_firstname_match:
                users_ids_list.append(user.user_id)
    elif Option.NAME.value in options:
        extendeds_list = list(ExtendedStudents.select().where(ExtendedStudents.name.contains(options[Option.NAME.value])))
    elif Option.GROUP.value in options:
        groups_list = list(GroupsOfStudents.select().where(GroupsOfStudents.group == options[Option.GROUP.value]))
        compacts_list = list(CompactStudents.select().where(CompactStudents.group == options[Option.GROUP.value]))
        extendeds_list = list(ExtendedStudents.select().where(ExtendedStudents.group == options[Option.GROUP.value]))
    elif Option.BB_LOGIN.value in options:
        bbs_list = list(BBStudents.select().where(BBStudents.login.contains(options[Option.BB_LOGIN.value])))
    
    for user_id in users_ids_list:
        user: Any = GroupsOfStudents.get_or_none(GroupsOfStudents.user_id == user_id)
        
        if user is not None:
            groups_list.append(user)
            continue
        
        user = CompactStudents.get_or_none(CompactStudents.user_id == user_id)
        
        if user is not None:
            compacts_list.append(user)
            continue
        
        user = ExtendedStudents.get_or_none(ExtendedStudents.user_id == user_id)
        
        if user is not None:
            extendeds_list.append(user)
            continue
        
        user = BBStudents.get_or_none(BBStudents.user_id == user_id)
        
        if user is not None:
            bbs_list.append(user)
            continue
        
        user = Users.get_or_none(Users.user_id == user_id)
        
        if user is not None:
            undefined_users_list.append(user)
    
    await show_users_list(
        users_type=Value.GROUPS.value, type_users_list=groups_list,
        loading_message=loading_message, message=message
    )
    await show_users_list(
        users_type=Value.COMPACTS.value, type_users_list=compacts_list,
        loading_message=loading_message, message=message
    )
    await show_users_list(
        users_type=Value.EXTENDEDS.value, type_users_list=extendeds_list,
        loading_message=loading_message, message=message
    )
    await show_users_list(
        users_type=Value.BBS.value, type_users_list=bbs_list,
        loading_message=loading_message, message=message
    )
    await show_users_list(
        users_type=Value.UNDEFINED.value, type_users_list=undefined_users_list,
        loading_message=loading_message, message=message
    )
    
    shown_users_number: int = sum([ len(groups_list), len(compacts_list), len(extendeds_list), len(bbs_list) ])
    
    await loading_message.delete()
    
    if shown_users_number == 0:
        await message.answer(text="No user matches the options!")
    else:
        await message.answer(
            text="*{shown}/{total}* users {auxiliary} shown!".format(
                shown=shown_users_number,
                total=len(Users),
                auxiliary="was" if shown_users_number == 1 else "were"
            ),
            parse_mode="markdown"
        )


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.METRICS.value ]
)
async def metrics(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text)
    
    if Option.DATE.value in options:
        if not compile("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$").match(options[Option.DATE.value]):
            await message.answer(
                text=(
                    "Incorrect date format!\n"
                    "It should be the following: `yyyy-mm-dd`"
                ),
                parse_mode="markdown"
            )
            return
        
        month_date: str = "".join([ options[Option.DATE.value][:-2], "*" ])
        day_date: str = options[Option.DATE.value]
    elif Option.MONTH.value in options:
        if not compile("^[0-9][0-9][0-9][0-9]-[0-9][0-9]$").match(options[Option.MONTH.value]):
            await message.answer(
                text=(
                    "Incorrect month format!\n"
                    "It should be the following: `yyyy-mm`"
                ),
                parse_mode="markdown"
            )
            return
        
        month: str = "-".join([ options[Option.MONTH.value], "*" ])
        
        month_metrics: List[Metrics] = Metrics.select().where(Metrics.date.regexp(month))
        graph_values: Dict[str, int] = {}
        
        for day_metrics in month_metrics:
            graph_values[day_metrics.date[5:]] = sum([
                day_metrics.classes,
                day_metrics.score,
                day_metrics.lecturers,
                day_metrics.notes,
                day_metrics.week,
                day_metrics.exams,
                day_metrics.dice,
                day_metrics.locations,
                day_metrics.brs,
                day_metrics.settings,
                day_metrics.help,
                day_metrics.donate,
                day_metrics.cancel,
                day_metrics.start,
                day_metrics.login,
                day_metrics.unknown_nontext_message,
                day_metrics.unknown_text_message,
                day_metrics.unknown_callback,
                day_metrics.no_permissions,
                day_metrics.unlogin
            ])
        
        PERIOD: int = 20
        max_requests_number: int = max(graph_values.values()) if len(graph_values.values()) != 0 else 0
        get_bar_length: Callable = lambda requests_number: int(requests_number/max_requests_number * PERIOD)
        
        graph: str = "\n".join(sorted([
            "• {day}: {requests_number:<4} {pluses}".format(
                day=date.split("-")[1],
                requests_number=requests_number,
                pluses="".join([ "+" for _ in range(get_bar_length(requests_number) if get_bar_length(requests_number) > 1 else 1) ])
            ) for (date, requests_number) in graph_values.items()
        ], key=lambda string_date: string_date[2:7], reverse=True))
        
        await message.answer(
            text=MONTH_GRAPH.format(
                month=MONTHS_EN.get(options[Option.MONTH.value].split("-")[1], "Unknown Month"),
                hashtag="metrics",
                graph=graph if graph != "" else "empty",
                total=sum(graph_values.values()),
                average=round(sum(graph_values.values())/len(graph_values.values()))
            ),
            parse_mode="markdown"
        )
        return
    else:
        month_date: str = datetime.today().strftime("%Y-%m-*")
        day_date: str = datetime.today().strftime("%Y-%m-%d")
    
    monthly_metrics: List[Metrics] = Metrics.select().where(Metrics.date.regexp(month_date))
    
    if not monthly_metrics.exists():
        await message.answer(
            text="No metrics for the asked date was found.",
            parse_mode="markdown"
        )
        return
    
    monthly_command_requests_stats_filling: Dict[str, int] = {
        "classes_monthly": sum([ day_metrics.classes for day_metrics in monthly_metrics ]),
        "score_monthly": sum([ day_metrics.score for day_metrics in monthly_metrics ]),
        "lecturers_monthly": sum([ day_metrics.lecturers for day_metrics in monthly_metrics ]),
        "notes_monthly": sum([ day_metrics.notes for day_metrics in monthly_metrics ]),
        "week_monthly": sum([ day_metrics.week for day_metrics in monthly_metrics ]),
        "exams_monthly": sum([ day_metrics.exams for day_metrics in monthly_metrics ]),
        "dice_monthly": sum([ day_metrics.dice for day_metrics in monthly_metrics ]),
        "locations_monthly": sum([ day_metrics.locations for day_metrics in monthly_metrics ]),
        "brs_monthly": sum([ day_metrics.brs for day_metrics in monthly_metrics ]),
        "settings_monthly": sum([ day_metrics.settings for day_metrics in monthly_metrics ]),
        "help_monthly": sum([ day_metrics.help for day_metrics in monthly_metrics ]),
        "donate_monthly": sum([ day_metrics.donate for day_metrics in monthly_metrics ]),
        "cancel_monthly": sum([ day_metrics.cancel for day_metrics in monthly_metrics ]),
        "start_monthly": sum([ day_metrics.start for day_metrics in monthly_metrics ]),
        "login_monthly": sum([ day_metrics.login for day_metrics in monthly_metrics ]),
        "unknown_nontext_message_monthly": sum([ day_metrics.unknown_nontext_message for day_metrics in monthly_metrics ]),
        "unknown_text_message_monthly": sum([ day_metrics.unknown_text_message for day_metrics in monthly_metrics ]),
        "unknown_callback_monthly": sum([ day_metrics.unknown_callback for day_metrics in monthly_metrics ]),
        "no_permissions_monthly": sum([ day_metrics.no_permissions for day_metrics in monthly_metrics ]),
        "unlogin_monthly": sum([ day_metrics.unlogin for day_metrics in monthly_metrics ])
    }
    
    monthly_command_requests_stats_filling["total_monthly"] = sum([
        requests_number for (_, requests_number) in monthly_command_requests_stats_filling.items()
    ])
    
    (existing_metrics, created_metrics) = Metrics.get_or_create(date=day_date)
    daily_metrics: Metrics = created_metrics if existing_metrics is None else existing_metrics
    
    daily_command_requests_stats_filling: Dict[str, int] = {
        "classes_daily": daily_metrics.classes,
        "score_daily": daily_metrics.score,
        "lecturers_daily": daily_metrics.lecturers,
        "notes_daily": daily_metrics.notes,
        "week_daily": daily_metrics.week,
        "exams_daily": daily_metrics.exams,
        "dice_daily": daily_metrics.dice,
        "locations_daily": daily_metrics.locations,
        "brs_daily": daily_metrics.brs,
        "settings_daily": daily_metrics.settings,
        "help_daily": daily_metrics.help,
        "donate_daily": daily_metrics.donate,
        "cancel_daily": daily_metrics.cancel,
        "start_daily": daily_metrics.start,
        "login_daily": daily_metrics.login,
        "unknown_nontext_message_daily": daily_metrics.unknown_nontext_message,
        "unknown_text_message_daily": daily_metrics.unknown_text_message,
        "unknown_callback_daily": daily_metrics.unknown_callback,
        "no_permissions_daily": daily_metrics.no_permissions,
        "unlogin_daily": daily_metrics.unlogin
    }
    
    daily_command_requests_stats_filling["total_daily"] = sum([
        requests_number for (_, requests_number) in daily_command_requests_stats_filling.items()
    ])
    
    await message.answer(
        text=COMMAND_REQUESTS_STATS.format(
            **daily_command_requests_stats_filling,
            **monthly_command_requests_stats_filling
        ),
        parse_mode="markdown"
    )
