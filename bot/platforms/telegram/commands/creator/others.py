from typing import Dict
from typing import List

from datetime import date
from datetime import datetime

from re import match

from peewee import ModelSelect

from aiogram.types import Message
from aiogram.types import ContentType
from aiogram.types import ParseMode
from aiogram.utils.exceptions import TelegramAPIError

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.commands.creator.utilities.helpers import parse_creator_query
from bot.platforms.telegram.commands.creator.utilities.helpers import update_progress_bar
from bot.platforms.telegram.commands.creator.utilities.constants import CREATOR_TELEGRAM_ID
from bot.platforms.telegram.commands.creator.utilities.constants import BROADCAST_MESSAGE_TEMPLATE
from bot.platforms.telegram.commands.creator.utilities.constants import MAX_TEXT_LENGTH
from bot.platforms.telegram.commands.creator.utilities.constants import MAX_CAPTION_LENGTH
from bot.platforms.telegram.commands.creator.utilities.types import Option
from bot.platforms.telegram.commands.creator.utilities.types import Value

from bot.models.user import User
from bot.models.day_off import DayOff
from bot.models.donation import Donation

from bot.utilities.types import Command
from bot.utilities.calendar.constants import MONTHS


@dispatcher.message_handler(
    lambda message:
        message.from_user.id == CREATOR_TELEGRAM_ID and
        Command.BROADCAST.value in (message.text or message.caption or ""),
    content_types=[ ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT ]
)
async def broadcast(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text or message.caption)
    
    if Option.MESSAGE.value not in options:
        await message.answer(text="No broadcast message was found!")
        return
    
    broadcast_text: str = options[Option.MESSAGE.value] if options.get(Option.SIGNED.value) == "false" else BROADCAST_MESSAGE_TEMPLATE.format(broadcast_message=options[Option.MESSAGE.value])
    
    if (
        message.content_type == ContentType.TEXT and len(broadcast_text) > MAX_TEXT_LENGTH
    ) or (any([
            message.content_type == ContentType.PHOTO,
            message.content_type == ContentType.VIDEO,
            message.content_type == ContentType.AUDIO,
            message.content_type == ContentType.DOCUMENT
        ]) and len(broadcast_text) > MAX_CAPTION_LENGTH
    ):
        await message.answer(text="The broadcast message is too long!")
        return
    
    users_ids_list: List[int] = []
    telegram_users: ModelSelect = User.select().where(~User.telegram_id.is_null())
    
    if "&" in options[Option.USERS.value]:
        for possible_id in options[Option.USERS.value].split("&"):
            if not possible_id.isdigit():
                await message.answer(
                    text="*{non_id}* cannot be user ID!".format(non_id=possible_id),
                    parse_mode=ParseMode.MARKDOWN
                )
                continue
            
            asked_id: int = int(possible_id)
            
            if not telegram_users.where(User.user_id == asked_id).exists():
                await message.answer(
                    text="*{id}* was not found!".format(id=asked_id),
                    parse_mode=ParseMode.MARKDOWN
                )
                continue
            
            users_ids_list.append(asked_id)
    elif options[Option.USERS.value] == Value.ME.value:
        users_ids_list.append(User.get(User.telegram_id == message.chat.id).user_id)
    elif options[Option.USERS.value] == Value.ALL.value:
        users_ids_list = [ user.user_id for user in telegram_users ]
    elif options[Option.USERS.value] == Value.GROUPS.value:
        users_ids_list = [ group.user_id for group in telegram_users.where(User.is_group_chat) ]
    elif options[Option.USERS.value] == Value.COMPACTS.value:
        users_ids_list = [ compact.user_id for compact in telegram_users.where(~User.is_group_chat & User.bb_login.is_null() & User.bb_password.is_null()) ]
    elif options[Option.USERS.value] == Value.BBS.value:
        users_ids_list = [ bb.user_id for bb in telegram_users.where(User.bb_login.is_null(False) & User.bb_password.is_null(False)) ]
    else:
        await message.answer(text="The option has no matches!")
        return
    
    loading_message: Message = await message.answer(text="Started broadcasting…")
    progress_bar: str = ""

    total_users_number: int = len(users_ids_list)
    unreachable_users_number: int = 0
    
    for (index, user_id) in enumerate(users_ids_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values_number=len(users_ids_list), index=index
        )
        
        user: User = User.get(User.user_id == user_id)
        
        try:
            if message.content_type == ContentType.TEXT:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=broadcast_text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
            elif message.content_type == ContentType.PHOTO:
                await message.bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=message.photo[0].file_id,
                    caption=broadcast_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            elif message.content_type == ContentType.VIDEO:
                await message.bot.send_video(
                    chat_id=user.telegram_id,
                    video=message.video.file_id,
                    caption=broadcast_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            elif message.content_type == ContentType.AUDIO:
                await message.bot.send_audio(
                    chat_id=user.telegram_id,
                    audio=message.audio.file_id,
                    caption=broadcast_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            elif message.content_type == ContentType.DOCUMENT:
                await message.bot.send_document(
                    chat_id=user.telegram_id,
                    document=message.document.file_id,
                    caption=broadcast_text,
                    parse_mode=ParseMode.MARKDOWN
                )
        except TelegramAPIError:
            unreachable_users_number += 1
    
    await loading_message.delete()
    
    await message.answer(
        text=f"Broadcasted to *{total_users_number - unreachable_users_number}* users out of {total_users_number}!",
        parse_mode=ParseMode.MARKDOWN
    )

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR_TELEGRAM_ID,
    commands=[ Command.DAYSOFF.value ]
)
async def daysoff(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text)
    
    if options.get(Option.EMPTY.value) == Value.LIST.value:
        days_off_list: List[DayOff] = list(DayOff.select())
        days_off_list.sort(key=lambda day_off: day_off.day.split("-")[::-1])

        days_off_text: str = "There are no dayoffs!" if len(days_off_list) == 0 else "*Days Off*\n_all kinds of_"
        
        current_month: str = ""
        previous_month: str = ""
        
        for day_off in days_off_list:
            current_month = MONTHS[day_off.day[3:5]]
            
            days_off_text = "".join([
                days_off_text,
                "" if previous_month == current_month else "".join([ "\n\n*выходные ", current_month, "*" ]),
                "\n• {day}: {day_off_message}".format(
                    day=int(day_off.day[0:2]),
                    day_off_message=day_off.message
                )
            ])
            
            previous_month = MONTHS[day_off.day[3:5]]
        
        await message.answer(
            text=days_off_text,
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if Option.ADD.value in options:
        asked_day: str = options[Option.ADD.value]
    elif Option.DROP.value in options:
        asked_day: str = options[Option.DROP.value]
        
        if asked_day == Value.ALL.value:
            dropped_days_off_number: int = DayOff.delete().execute()
            
            await message.answer(
                text="*{dropped_days_off_number}* were dropped!".format(dropped_days_off_number=dropped_days_off_number),
                parse_mode=ParseMode.MARKDOWN
            )
            return
    else:
        await message.answer(text="No options were found!")
        return
    
    if match("^[0-9][0-9]-[0-9][0-9]$", asked_day) is None:
        await message.answer(
            text=(
                "Incorrect date format!\n"
                "It should be the following: `dd-mm`"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    asked_day_off: DayOff = DayOff.get_or_none(DayOff.day == asked_day)
    text: str = "Done!"
    
    if Option.ADD.value in options:
        if asked_day_off is None:
            DayOff.insert(day=asked_day, message=options[Option.MESSAGE.value] if Option.MESSAGE.value in options else "Выходной").execute()
        else:
            text = "{day_off_date} day off have been added already!".format(day_off_date=asked_day)
    elif Option.DROP.value in options:
        if asked_day_off is not None:
            asked_day_off.delete_instance()
        else:
            text = "{day_off_date} is not a day off!".format(day_off_date=asked_day)
    
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR_TELEGRAM_ID,
    commands=[ Command.DONATED.value ]
)
async def donated(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text)
    
    if Option.AMOUNT.value not in options:
        await message.answer(text="Amount of donate was not provided!")
        return
    if Option.DONATOR.value not in options:
        await message.answer(text="Donator's name was not provided!")
        return
    if Option.DATE.value not in options:
        await message.answer(text="Date of donation was not provided!")
        return
    
    amount_string: str = options[Option.AMOUNT.value]

    if not amount_string.replace(".", "", 1).isdigit():
        await message.answer(text="Incorrect amount of donate was provided!")
        return
    
    date_string: str = options[Option.DATE.value]

    if match(pattern="^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$", string=date_string) is None:
        await message.answer(
            text=(
                "Incorrect date format!\n"
                "It should be the following: `yyyy-mm-dd`"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    amount: float = float(amount_string)
    donation_date: date = datetime.strptime(date_string, "%Y-%m-%d").date()
    donator: str = options[Option.DONATOR.value]
    
    Donation.insert(amount=amount, date=donation_date, donator=donator).execute()
    
    await message.answer(
        text="Added!",
        parse_mode=ParseMode.MARKDOWN
    )
