from typing import Optional
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

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.commands.creator.utilities.constants import PROGRESS_BAR_PERIOD


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
    percent: int = int((index + 1)/values_number*PROGRESS_BAR_PERIOD)
    
    next_progress_bar: str = "`[ {pluses}{minuses} ]`".format(
        pluses="".join([ "+" for _ in range(percent) ]),
        minuses="".join([ "-" for _ in range(PROGRESS_BAR_PERIOD - percent) ])
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
        chat = await dispatcher.bot.get_chat(chat_id=chat_id)
        is_chat_action_successfully_sent = dispatcher.bot.send_chat_action(chat_id=chat_id, action="typing")
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
