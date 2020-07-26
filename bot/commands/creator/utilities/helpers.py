from aiogram.types import Message
from aiogram.types import Chat

from aiogram.utils.exceptions import CantInitiateConversation
from aiogram.utils.exceptions import UserDeactivated
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.exceptions import BotKicked
from aiogram.utils.exceptions import ChatNotFound

from bot import bot
from bot import students

from bot.commands.creator.utilities.constants import USER_DATA
from bot.commands.creator.utilities.types import Option
from bot.commands.creator.utilities.types import Suboption

from bot.shared.api.student import Student


async def update_progress_bar(loading_message, current_progress_bar: str, values: [Student], index: int) -> str:
    period: int = 20
    percent: int = int((index + 1)/len(values)*period)
    
    next_progress_bar: str = "`[ {plus}{minus} ]`".format(
        plus="".join([ "+" for _ in range(percent) ]),
        minus="".join([ "-" for _ in range(period - percent) ])
    )
    
    if current_progress_bar == next_progress_bar: return current_progress_bar
    
    await loading_message.edit_text(
        text=next_progress_bar,
        parse_mode="markdown"
    )
    
    return next_progress_bar


def parse_creator_query(query: str) -> {str: str}:
    query_array: [str] = query.split(" ")
    query_dictionary: {str: str} = {}
    
    key: str = ""
    value: str = ""
    
    index: int = 0
    
    while index < len(query_array):
        if query_array[index].endswith(":"):
            (key, value) = (query_array[index][:-1], "")
        else:
            while index < len(query_array) and not query_array[index].endswith(":"):
                value = " ".join([ value, query_array[index] ])
                index += 1
            index -= 1
            
            query_dictionary[key] = value[1:]
        
        index += 1
    
    return query_dictionary


async def collect_ids(query_message: Message) -> [int]:
    options: { str: str } = parse_creator_query(query_message.get_args())
    
    if Option.IDS.value not in options:
        await query_message.answer(
            text="*ids* option has not been found!",
            parse_mode="markdown"
        )
        return []
    
    if options[Option.IDS.value] == Suboption.ALL.value:
        return list(students)
    if Suboption.UNLOGIN.value in options[Option.IDS.value]:
        return [ chat_id for chat_id in students if not students[chat_id].is_setup ]
    if Suboption.ME.value in options[Option.IDS.value]:
        return [ query_message.chat.id ]
    if Suboption.EXTENDED.value in options[Option.IDS.value]:
        return [ chat_id for chat_id in students if students[chat_id].type is Student.Type.EXTENDED ]
    if Suboption.COMPACT.value in options[Option.IDS.value]:
        return [ chat_id for chat_id in students if students[chat_id].type is Student.Type.COMPACT ]
    if Suboption.GROUP_CHAT.value in options[Option.IDS.value]:
        return [ chat_id for chat_id in students if students[chat_id].type is Student.Type.GROUP_CHAT ]
    
    users_list: [int] = []
    
    for possible_chat_id in options[Option.IDS.value].split("&"):
        try:
            chat_id: int = int(possible_chat_id)
        except ValueError:
            await query_message.answer(
                text="*{non_chat_id}* cannot be a chat id!".format(non_chat_id=possible_chat_id),
                parse_mode="markdown"
            )
        else:
            users_list.append(chat_id)
    
    return users_list


async def try_get_chat(chat_id: int) -> (Chat, str):
    chat: Chat = None
    error_text: str = None
    
    try:
        chat = await bot.get_chat(chat_id=chat_id)
    except CantInitiateConversation:
        error_text = "User {chat_id} have never initiated a conversation with the bot.".format(chat_id=chat_id)
    except UserDeactivated:
        error_text = "User {chat_id} is deactivated.".format(chat_id=chat_id)
    except BotBlocked:
        error_text = "User {chat_id} blocked the bot.".format(chat_id=chat_id)
    except BotKicked:
        error_text = "Bot was kicked from {chat_id} group chat.".format(chat_id=chat_id)
    except ChatNotFound:
        error_text = "Couldn't find {chat_id} chat.".format(chat_id=chat_id)
    
    return (chat, error_text)


def get_user_data(student: Student, hashtag: str, chat_id: int, chat: Chat = None) -> str:
    return USER_DATA.format(
        fullname="none" if chat is None else chat.full_name, username="none" if chat is None else chat.username,
        chat_id=chat_id,
        type="none" if student.type is None else student.type.value,
        institute=student.institute,
        year=student.year,
        group_number=student.group,
        name=student.name,
        card=student.card,
        notes_number=len(student.notes),
        edited_classes_number=len(student.edited_subjects),
        fellow_students_number=len(student.group_names),
        guard_text=student.guard.text,
        guard_message="none" if student.guard.message is None else student.guard.message.text,
        hashtag=hashtag
    )
