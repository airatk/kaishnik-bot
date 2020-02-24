from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.creator.utilities.helpers import parse_creator_query
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.helpers import collect_users_list
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import BROADCAST_MESSAGE_TEMPLATE

from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import IS_WEEK_REVERSED_FILE
from bot.shared.data.constants import DAYOFFS
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.BROADCAST.value ]
)
async def broadcast(message: Message):
    options: {str: str} = parse_creator_query(message.text)
    
    if "message" not in options:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No broadcast message was found!"
        )
        return
    
    broadcast_list: [Student] = await collect_users_list(query_message=message)
    
    progress_bar: str = ""
    
    loading_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text="Started broadcasting..."
    )
    
    for (index, chat_id) in enumerate(broadcast_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=broadcast_list, index=index
        )
        
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=options["message"] if "false" == options.get("signed") else BROADCAST_MESSAGE_TEMPLATE.format(broadcast_message=options["message"]),
                parse_mode="markdown",
                disable_web_page_preview=True
            )
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="{} is inactive! /clear?".format(chat_id)
            )
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Broadcasted to *{}* users!".format(len(broadcast_list)),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.REVERSE.value ]
)
async def reverse(message: Message):
    if "week" not in message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to reverse type of a week, type */reverse week*",
            parse_mode="markdown"
        )
        return
    
    save_data(file=IS_WEEK_REVERSED_FILE, object=not load_data(file=IS_WEEK_REVERSED_FILE))
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Week was #reversed!"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DAYOFF.value ]
)
async def dayoff(message: Message):
    options: {str: str} = parse_creator_query(message.text)
    
    daysoffs: [(int, int)] = load_data(file=DAYOFFS)
    
    if "add" in options:
        raw_date: str = options["add"]
    elif "drop" in options:
        raw_date: str = options["drop"]
        
        if raw_date == "all":
            save_data(file=DAYOFFS, object=[])
            
            await bot.send_message(
                chat_id=message.chat.id,
                text="Dropped!"
            )
            
            return
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No options were found!"
        )
        return
    
    try:
        parsed_date: [str] = raw_date.split("-")
        dayoff: (int, int) = (int(parsed_date[0]), int(parsed_date[1]))
    except Exception:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Write date in following format: *26-07*",
            parse_mode="markdown"
        )
        return
    
    if "add" in options:
        daysoffs.append(dayoff)
    elif "drop" in options:
        try:
            daysoffs.remove(dayoff)
        except ValueError:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Not a dayoff!"
            )
            return
    
    save_data(file=DAYOFFS, object=daysoffs)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Done!"
    )
