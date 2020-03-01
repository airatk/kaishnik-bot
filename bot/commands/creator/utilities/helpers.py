from aiogram.types import Message

from bot import students

from bot.commands.creator.utilities.types import Suboption

from bot.shared.api.student import Student


def parse_creator_query(query: str) -> {str: str}:
    query_array: [str] = query.split()
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


async def collect_users_list(query_message: Message) -> [int]:
    options: { str: str } = parse_creator_query(query_message.get_args())

    if "ids" not in options:
        await query_message.answer(text="`ids` option has not been found!")
        return []
    
    if options["ids"] == Suboption.ALL.value: return list(students)
    
    users_list: [int] = []
    
    if Suboption.UNLOGIN.value in options["ids"]:
        users_list += [ chat_id for chat_id in list(students) if not students[chat_id].is_setup ]
    elif Suboption.ME.value in options["ids"]:
        users_list.append(query_message.chat.id)
    
    for possible_chat_id in options["ids"].split("&"):
        try:
            chat_id: int = int(possible_chat_id)
        except Exception:
            pass
        else:
            users_list.append(chat_id)
    
    return users_list
