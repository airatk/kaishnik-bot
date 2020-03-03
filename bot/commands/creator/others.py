from aiogram.types import Message
from aiogram.utils.exceptions import ChatNotFound

from bot import dispatcher

from bot.commands.creator.utilities.helpers import parse_creator_query
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.helpers import collect_users_list
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import BROADCAST_MESSAGE_TEMPLATE

from bot.shared.api.student import Student
from bot.shared.calendar.constants import MONTHS
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
    options: {str: str} = parse_creator_query(message.get_args())
    
    if "message" not in options:
        await message.answer(text="No broadcast message was found!")
        return
    
    broadcast_list: [Student] = await collect_users_list(query_message=message)
    
    progress_bar: str = ""
    
    loading_message: Message = await message.answer(text="Started broadcasting...")
    
    for (index, chat_id) in enumerate(broadcast_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=broadcast_list, index=index
        )
        
        try:
            await message.answer(
                text=options["message"] if options.get("signed") == "false" else BROADCAST_MESSAGE_TEMPLATE.format(broadcast_message=options["message"]),
                parse_mode="markdown",
                disable_web_page_preview=True
            )
        except ChatNotFound:
            await message.answer(text="{} is inactive! /clear?".format(chat_id))
    
    await message.answer(
        text="Broadcasted to *{}* users!".format(len(broadcast_list)),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.REVERSE.value ]
)
async def reverse(message: Message):
    if "week" not in message.text:
        await message.answer(
            text="If you are sure to reverse type of a week, type */reverse week*",
            parse_mode="markdown"
        )
        return
    
    save_data(file=IS_WEEK_REVERSED_FILE, object=not load_data(file=IS_WEEK_REVERSED_FILE))
    
    await message.answer(text="Week was #reversed!")

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DAYOFF.value ]
)
async def dayoff(message: Message):
    options: {str: str} = parse_creator_query(message.get_args())
    
    dayoff_dates: {(int, int)} = load_data(file=DAYOFFS)
    
    if options.get("") == "list":
        dayoffs_list: str = "There are no dayoffs!" if len(dayoff_dates) == 0 else "*Dayoffs*\n"
        
        for (day_index, month_index) in dayoff_dates:
            month: str = MONTHS["{month_index:02}".format(month_index=month_index)]
            dayoffs_list = "\n".join([ dayoffs_list, "• {day} {month}".format(day=day_index, month=month) ])
        
        await message.answer(
            text=dayoffs_list,
            parse_mode="markdown"
        )
    elif "add" in options or "drop" in options:
        if "add" in options:
            raw_date: str = options["add"]
        elif "drop" in options:
            raw_date: str = options["drop"]
            
            if raw_date == "all":
                save_data(file=DAYOFFS, object=[])
                await message.answer(text="Dropped!")
                return
        
        parsed_date: [str] = raw_date.split("-")
        
        try:
            dayoff_date: (int, int) = (int(parsed_date[0]), int(parsed_date[1]))
        except ValueError:
            await message.answer(
                text="Write date in the following format: *26-07*",
                parse_mode="markdown"
            )
            return
        
        if "add" in options:
            if dayoff_date not in dayoff_dates:
                dayoff_dates.append(dayoff_date)
            else:
                await message.answer(text="The dayoff have been added already!")
                return
        elif "drop" in options:
            if dayoff_date in dayoff_dates:
                dayoff_dates.remove(dayoff_date)
            else:
                await message.answer(text="Not a dayoff!")
                return
        
        save_data(file=DAYOFFS, object=dayoff_dates)
        await message.answer(text="Done!")
    else:
        await message.answer(text="No options were found!")
