from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.creator.utilities.helpers import parse_creator_request
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import BROADCAST_MESSAGE_TEMPLATE
from bot.commands.creator.utilities.types import ReverseOption

from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import IS_WEEK_REVERSED_FILE
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.BROADCAST.value ]
)
async def broadcast(message: Message):
    if message.text == "/broadcast":
        await bot.send_message(
            chat_id=message.chat.id,
            text="No broadcast message was found! It's supposed to be right after the */broadcast* command.",
            parse_mode="markdown"
        )
        return
    
    broadcast_message: str = message.text[11:]  # Getting rid of /boardcast command
    progress_bar: str = ""
    students_list: [Student] = list(students)
    
    loading_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text="Started broadcasting..."
    )
    
    for (index, chat_id) in enumerate(students_list):
        progress_bar = update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=students_list, index=index
        )
        
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=BROADCAST_MESSAGE_TEMPLATE.format(broadcast_message=broadcast_message),
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
        text="Broadcasted!"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.REVERSE.value ]
)
async def reverse(message: Message):
    (option, _) = parse_creator_request(message.text)
    
    if option == ReverseOption.WEEK.value:
        save_data(file=IS_WEEK_REVERSED_FILE, object=not load_data(file=IS_WEEK_REVERSED_FILE))
        
        await bot.send_message(
            chat_id=message.chat.id,
            text="Week was #reversed!"
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to reverse type of a week, type */reverse week*",
            parse_mode="markdown"
        )
