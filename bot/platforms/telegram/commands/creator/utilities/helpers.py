from typing import Optional
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from aiogram.types import Message
from aiogram.types import Chat
from aiogram.types import ParseMode

from aiogram.utils.exceptions import CantInitiateConversation
from aiogram.utils.exceptions import UserDeactivated
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.exceptions import BotKicked
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.exceptions import TelegramAPIError

from bot.platforms.telegram import telegram_bot
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.creator.utilities.types import Value

from bot.models.users import Users
from bot.models.notes import Notes


def parse_creator_query(query: str) -> Dict[str, str]:
    query_list: List[str] = query.split(" ")[1:]  # Getting rid of a command in the query
    
    query_dictionary: Dict[str, str] = {}
    key: str = ""
    
    for word in query_list:
        if word == ":":
            query_dictionary[key] = "".join([ query_dictionary.get(key, ""), word ])
        elif word.endswith(":"):
            key = word[:-1]
            query_dictionary[key] = ""
        elif query_dictionary.get(key, "") == "":
            query_dictionary[key] = word
        else:
            query_dictionary[key] = " ".join([ query_dictionary[key], word ])
    
    return query_dictionary

async def update_progress_bar(loading_message: Message, current_progress_bar: str, values_number: int, index: int) -> str:
    PERIOD: int = 20
    percent: int = int((index + 1)/values_number*PERIOD)
    
    next_progress_bar: str = "`[ {pluses}{minuses} ]`".format(
        pluses="".join([ "+" for _ in range(percent) ]),
        minuses="".join([ "-" for _ in range(PERIOD - percent) ])
    )
    
    if current_progress_bar == next_progress_bar: return current_progress_bar
    
    await loading_message.edit_text(
        text=next_progress_bar,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return next_progress_bar

async def try_get_chat(chat_id: int) -> Tuple[Chat, str]:
    chat: Optional[Chat] = None
    is_chat_action_successfully_sent: bool = False
    error_text: Optional[str] = None
    
    try:
        chat = await telegram_bot.get_chat(chat_id=chat_id)
        is_chat_action_successfully_sent = telegram_bot.send_chat_action(chat_id=chat_id, action="typing")
    except CantInitiateConversation:
        error_text = "User {chat_id} have never initiated a conversation with the bot."
    except UserDeactivated:
        error_text = "User {chat_id} is deactivated."
    except BotBlocked:
        error_text = "User {chat_id} blocked the bot."
    except BotKicked:
        error_text = "Bot was kicked from {chat_id} group chat."
    except ChatNotFound:
        error_text = "Couldn't find {chat_id} chat."
    except TelegramAPIError:
        error_text = "Unknown error causes unavailability of {chat_id} chat."
    else:
        if not is_chat_action_successfully_sent:
            chat = None
            error_text = "Couldn't send a chat action to user {chat_id}"
    
    return (chat, None if error_text is None else error_text.format(chat_id=chat_id))

async def show_users_list(users_type: str, type_users_list: List[Any], loading_message: Message, message: Message):
    await loading_message.edit_text(text="Started showing {users_type} users…".format(users_type=users_type))
    
    progress_bar: str = ""
    
    for (index, type_user) in enumerate(type_users_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values_number=len(type_users_list), index=index
        )
        
        user: Users = Users.get(Users.user_id == type_user.user_id)
        (chat, error_message) = await try_get_chat(chat_id=user.telegram_id)
        
        if users_type == Value.GROUPS.value:
            type_user_data: str = (
                "• Group: {group}\n"
                "• Group Schedule ID: {group_schedule_id}\n"
            ).format(
                group=type_user.group,
                group_schedule_id=type_user.group_schedule_id
            )
        elif users_type == Value.COMPACTS.value:
            type_user_data: str = (
                "• Group: {group}\n"
                "• Group Schedule ID: {group_schedule_id}\n"
            ).format(
                group=type_user.group,
                group_schedule_id=type_user.group_schedule_id
            )
        elif users_type == Value.EXTENDEDS.value:
            type_user_data: str = (
                "• Institute: {institute}\n"
                "• Institute ID: {institute_id}\n"
                "• Year: {year}\n"
                "• Group: {group}\n"
                "• Group Schedule ID: {group_schedule_id}\n"
                "• Group Score ID: {group_score_id}\n"
                "• Name: {name}\n"
                "• Name ID: {name_id}\n"
                "• Card: {card}\n"
            ).format(
                institute=type_user.institute,
                institute_id=type_user.institute_id,
                year=type_user.year,
                group=type_user.group,
                group_schedule_id=type_user.group_schedule_id,
                group_score_id=type_user.group_score_id,
                name=type_user.name,
                name_id=type_user.name_id,
                card=type_user.card
            )
        elif users_type == Value.BBS.value:
            type_user_data: str = (
                "• Login: {login}\n"
                "• Password: {password}\n"
            ).format(
                login=type_user.login,
                password=type_user.password
            )
        else:
            type_user_data: str = "Undefined user type.\n"
        
        await message.answer(
            text="".join([
                "" if error_message is None else "".join([ error_message, "\n\n" ]), (
                    "{fullname} @{username}\n"
                    "{users_type}\n"
                    "\n"
                    "• User ID: {user_id}\n"
                    "\n"
                ).format(
                    fullname="none" if chat is None else chat.full_name,
                    username="none" if chat is None else chat.username,
                    users_type=users_type,
                    user_id=type_user.user_id
                ),
                type_user_data,
                "\n", (
                    "• Notes: {notes_number}\n"
                    "\n"
                    "• Guard text: {guard_text}\n"
                    "• Guard message: {guard_message}\n"
                    "\n"
                    "• Is Setup: {is_setup}\n"
                    "\n"
                    "/erase_{user_id}\n"
                    "\n"
                    "#data"
                ).format(
                    notes_number=Notes.select().where(Notes.user_id == type_user.user_id).count(),
                    guard_text="none" if guards[user.telegram_id].text is None else guards[user.telegram_id].text,
                    guard_message="none" if guards[user.telegram_id].message is None else guards[user.telegram_id].message.text,
                    is_setup=user.is_setup,
                    user_id=type_user.user_id
                )
            ])
        )
