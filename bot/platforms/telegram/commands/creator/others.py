from re import compile

from typing import Dict
from typing import List

from aiogram.types import Message
from aiogram.types import ContentType

from aiogram.utils.exceptions import TelegramAPIError

from bot.platforms.telegram import dispatcher

from bot.platforms.telegram.commands.creator.utilities.helpers import parse_creator_query
from bot.platforms.telegram.commands.creator.utilities.helpers import update_progress_bar
from bot.platforms.telegram.commands.creator.utilities.constants import CREATOR
from bot.platforms.telegram.commands.creator.utilities.constants import BROADCAST_MESSAGE_TEMPLATE
from bot.platforms.telegram.commands.creator.utilities.constants import MAX_TEXT_LENGTH
from bot.platforms.telegram.commands.creator.utilities.constants import MAX_CAPTION_LENGTH
from bot.platforms.telegram.commands.creator.utilities.types import Option
from bot.platforms.telegram.commands.creator.utilities.types import Value

from bot.models.users import Users
from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents
from bot.models.days_off import DaysOff

from bot.utilities.types import Commands
from bot.utilities.calendar.constants import MONTHS


@dispatcher.message_handler(
    lambda message:
        message.from_user.id == CREATOR and
        Commands.BROADCAST.value in (message.text or message.caption or ""),
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
    
    if "&" in options[Option.USERS.value]:
        for possible_id in options[Option.USERS.value].split("&"):
            try:
                asked_id: int = int(possible_id)
            except ValueError:
                await message.answer(
                    text="*{non_id}* cannot be user ID!".format(non_id=possible_id),
                    parse_mode="markdown"
                )
                continue
            else:
                if not Users.select().where(Users.user_id == asked_id).exists():
                    await message.answer(
                        text="*{id}* was not found!".format(id=asked_id),
                        parse_mode="markdown"
                    )
                    continue
                
                users_ids_list.append(asked_id)
    elif options[Option.USERS.value] == Value.ME.value:
        users_ids_list.append(Users.get(Users.telegram_id == message.chat.id))
    elif options[Option.USERS.value] == Value.ALL.value:
        users_ids_list = [ user.user_id for user in Users.select() ]
    elif options[Option.USERS.value] == Value.GROUPS.value:
        users_ids_list = [ group.user_id for group in GroupsOfStudents.select() ]
    elif options[Option.USERS.value] == Value.COMPACTS.value:
        users_ids_list = [ compact.user_id for compact in CompactStudents.select() ]
    elif options[Option.USERS.value] == Value.EXTENDEDS.value:
        users_ids_list = [ extended.user_id for extended in ExtendedStudents.select() ]
    elif options[Option.USERS.value] == Value.BBS.value:
        users_ids_list = [ bb.user_id for bb in BBStudents.select() ]
    else:
        await message.answer(text="The option has no matches!")
        return
    
    loading_message: Message = await message.answer(text="Started broadcasting...")
    progress_bar: str = ""
    
    for (index, user_id) in enumerate(users_ids_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values_number=len(users_ids_list), index=index
        )
        
        user: Users = Users.get(Users.user_id == user_id)
        
        try:
            if message.content_type == ContentType.TEXT:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=broadcast_text,
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
            elif message.content_type == ContentType.PHOTO:
                await message.bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=message.photo[0].file_id,
                    caption=broadcast_text,
                    parse_mode="markdown"
                )
            elif message.content_type == ContentType.VIDEO:
                await message.bot.send_video(
                    chat_id=user.telegram_id,
                    video=message.video.file_id,
                    caption=broadcast_text,
                    parse_mode="markdown"
                )
            elif message.content_type == ContentType.AUDIO:
                await message.bot.send_audio(
                    chat_id=user.telegram_id,
                    audio=message.audio.file_id,
                    caption=broadcast_text,
                    parse_mode="markdown"
                )
            elif message.content_type == ContentType.DOCUMENT:
                await message.bot.send_document(
                    chat_id=user.telegram_id,
                    document=message.document.file_id,
                    caption=broadcast_text,
                    parse_mode="markdown"
                )
        except TelegramAPIError:
            user.delete_instance()
    
    await loading_message.delete()
    
    await message.answer(
        text="Broadcasted to *{users_number}* users!".format(users_number=len(users_ids_list)),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.DAYSOFF.value ]
)
async def daysoff(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text)
    
    if options.get(Option.EMPTY.value) == Value.LIST.value:
        days_off_list: List[DaysOff] = list(DaysOff.select())
        
        days_off_text: str = "There are no dayoffs!" if len(days_off_list) == 0 else "*Days Off*\n_all kinds of_"
        
        days_off_list.sort(key=lambda day_off: day_off.date.split("-")[::-1])
        
        current_month: str = ""
        previous_month: str = ""
        
        for day_off in days_off_list:
            current_month = MONTHS[day_off.date[3:5]]
            
            days_off_text = "".join([
                days_off_text,
                "" if previous_month == current_month else "".join([ "\n\n*выходные ", current_month, "*" ]),
                "\n• {day}: {day_off_message}".format(
                    day=int(day_off.date[0:2]),
                    day_off_message=day_off.message
                )
            ])
            
            previous_month = MONTHS[day_off.date[3:5]]
        
        await message.answer(
            text=days_off_text,
            parse_mode="markdown"
        )
        return
    
    if Option.ADD.value in options:
        asked_date: str = options[Option.ADD.value]
    elif Option.DROP.value in options:
        asked_date: str = options[Option.DROP.value]
        
        if asked_date == Value.ALL.value:
            dropped_days_off_number: int = DaysOff.delete().execute()
            
            await message.answer(
                text="*{dropped_days_off_number}* were dropped!".format(dropped_days_off_number=dropped_days_off_number),
                parse_mode="markdown"
            )
            return
    else:
        await message.answer(text="No options were found!")
        return
    
    if not compile("^[0-9][0-9]-[0-9][0-9]$").match(asked_date):
        await message.answer(
            text=(
                "Incorrect date format!\n"
                "It should be the following: `dd-mm`"
            ),
            parse_mode="markdown"
        )
        return
    
    asked_day_off: DaysOff = DaysOff.get_or_none(DaysOff.date == asked_date)
    text: str = "Done!"
    
    if Option.ADD.value in options:
        if asked_day_off is None:
            DaysOff.create(date=asked_date, message=options[Option.MESSAGE.value] if Option.MESSAGE.value in options else "Выходной")
        else:
            text = "{day_off_date} day off have been added already!".format(day_off_date=asked_date)
    elif Option.DROP.value in options:
        if asked_day_off is not None:
            asked_day_off.delete_instance()
        else:
            text = "{day_off_date} is not a day off!".format(day_off_date=asked_date)
    
    await message.answer(
        text=text,
        parse_mode="markdown"
    )
