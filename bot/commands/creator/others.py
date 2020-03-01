from aiogram.types import Message

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
                text=options["message"] if "false" == options.get("signed") else BROADCAST_MESSAGE_TEMPLATE.format(broadcast_message=options["message"]),
                parse_mode="markdown",
                disable_web_page_preview=True
            )
        except Exception:
            await message.answer(text="{} is inactive! /clear?".format(chat_id))
    
    await message.answer(
        text="Broadcasted to *{}* users!".format(len(broadcast_list)),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.POLL.value ]
)
async def poll(message: Message):
    options: {str, str} = parse_creator_query(message.get_agrs())
    
    if "question" not in options:
        await message.answer(text="No question was found!")
        return
    
    question: str = options["question"]
    
    if "answer1" not in options or "answer2" not in options:
        await message.answer(text="Poll gotta have at least 2 answers!")
        return
    
    answers: [str] = [ options["answer1"], options["answer2"] ]
    last_answer_id: int = 2
    
    while True:
        last_answer_id += 1
        answer_key: str = "answer{id}".format(id=last_answer_id)
        
        if answer_key not in options: break
        
        answers.append(options[answer_key])
    
    is_anonymous: bool = options.get("anonymous") == "true"
    allows_multiple_answers: bool = options.get("multipleanswers") == "true"
    is_closed: bool = options.get("closed") == "true"
    
    correct_option_id: str = options.get("correctoption")
    correct_option_id: int = int(correct_option_id) if correct_option_id is not None else None
    
    await message.bot.send_poll(
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
    
    dayoffs: {(int, int)} = load_data(file=DAYOFFS)
    
    if options.get("") == "list":
        dayoffs_list: str = "There are no dayoffs!" if len(dayoffs) == 0 else "*Dayoffs*\n"
        
        for (day_index, month_index) in dayoffs:
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
            dayoff: (int, int) = (int(parsed_date[0]), int(parsed_date[1]))
        except Exception:
            await message.answer(
                text="Write date in the following format: *26-07*",
                parse_mode="markdown"
            )
            return
        
        if "add" in options:
            if dayoff not in dayoffs:
                dayoffs.append(dayoff)
            else:
                await message.answer(text="The dayoff have been added already!")
                return
        elif "drop" in options:
            if dayoff in dayoffs:
                dayoffs.remove(dayoff)
            else:
                await message.answer(text="Not a dayoff!")
                return
        
        save_data(file=DAYOFFS, object=dayoffs)
        await message.answer(text="Done!")
    else:
        await message.answer(text="No options were found!")
