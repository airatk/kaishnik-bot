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
    commands=[ Commands.POLL.value ]
)
async def poll(message: Message):
    options: {str, str} = parse_creator_query(message.text)
    
    if "question" not in options:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No question was found!"
        )
        return
    
    question: str = options["question"]
    
    answer_id: int = 1
    answer_key: str = "answer1"
    answers: [str] = []
    
    if answer_key not in options:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No answers were found!"
        )
        return
    
    while answer_key in options:
        answers.append(options[answer_key])
        
        answer_id += 1
        answer_key = "answer{id}".format(id=answer_id)
    
    is_anonymous: bool = options.get("anonymous") == "true"
    allows_multiple_answers: bool = options.get("multipleanswers") == "true"
    is_closed: bool = options.get("closed") == "true"
    
    correct_option_id: str = options.get("correctoption")
    correct_option_id: int = int(correct_option_id) if correct_option_id is not None else None
    
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=is_anonymous,
        allows_multiple_answers=allows_multiple_answers,
        is_closed=is_closed,
        correct_option_id=correct_option_id
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
    
    dayoffs: {(int, int)} = load_data(file=DAYOFFS)
    
    if options.get("") == "list":
        dayoffs_list: str = "There are no dayoffs!" if len(dayoffs) == 0 else "*Dayoffs*\n"
        
        for (day_index, month_index) in dayoffs:
            month: str = MONTHS["{month_index:02}".format(month_index=month_index)]
            dayoffs_list = "\n".join([ dayoffs_list, "• {day} {month}".format(day=day_index, month=month) ])
        
        await bot.send_message(
            chat_id=message.chat.id,
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
                
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Dropped!"
                )
                
                return
        
        try:
            parsed_date: [str] = raw_date.split("-")
            dayoff: (int, int) = (int(parsed_date[0]), int(parsed_date[1]))
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Write date in the following format: *26-07*",
                parse_mode="markdown"
            )
            return
        
        if "add" in options:
            if dayoff not in dayoffs:
                dayoffs.append(dayoff)
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="The dayoff have been added already!"
                )
                return
        elif "drop" in options:
            if dayoff in dayoffs:
                dayoffs.remove(dayoff)
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Not a dayoff!"
                )
                return
        
        save_data(file=DAYOFFS, object=dayoffs)
        
        await bot.send_message(
            chat_id=message.chat.id,
            text="Done!"
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No options were found!"
        )
