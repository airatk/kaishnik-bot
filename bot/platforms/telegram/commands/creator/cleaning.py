from typing import Dict
from typing import List

from aiogram.types import Message

from aiogram.utils.exceptions import CantInitiateConversation
from aiogram.utils.exceptions import UserDeactivated
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.exceptions import BotKicked
from aiogram.utils.exceptions import ChatNotFound

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.creator.utilities.helpers import parse_creator_query
from bot.platforms.telegram.commands.creator.utilities.helpers import update_progress_bar
from bot.platforms.telegram.commands.creator.utilities.helpers import try_get_chat
from bot.platforms.telegram.commands.creator.utilities.constants import CREATOR
from bot.platforms.telegram.commands.creator.utilities.types import Option
from bot.platforms.telegram.commands.creator.utilities.types import Value

from bot.models.users import Users
from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents

from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.CLEAR.value ]
)
async def clear(message: Message):
    users_list: List[Users] = list(Users.select())
    cleared_users_number: int = 0
    
    loading_message: Message = await message.answer(text="Started clearing...")
    progress_bar: str = ""
    
    for (index, user) in enumerate(users_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values_number=len(users_list), index=index
        )
        
        (chat, error_message) = await try_get_chat(chat_id=user.telegram_id)
        
        if chat is None:
            await message.answer(text=error_message)
            
            user.delete_instance()
            cleared_users_number += 1
    
    await loading_message.delete()
    
    await message.answer(
        text=" ".join([
            str(cleared_users_number),
            "user was" if cleared_users_number == 1 else "users were",
            "#cleared!"
        ])
    )

@dispatcher.message_handler(
    lambda message:
        message.from_user.id == CREATOR and
        Commands.ERASE.value in message.text,
)
async def erase(message: Message):
    try:
        user_id: int = int(message.text.replace(Commands.ERASE.value, "")[1:])
    except ValueError:
        await message.answer(text="User ID should be integer!")
        return
    
    erased_users_number: int = Users.delete().where(Users.user_id == user_id).execute()
    
    if erased_users_number == 0:
        await message.answer(text="User ID was not found!")
    else:
        await message.answer(text="Erased!")

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.DROP.value ]
)
async def drop(message: Message):
    options: Dict[str, str] = parse_creator_query(query=message.text)
    
    if len(options) == 0:
        await message.answer(text="No options were found!")
        return
    
    if options[Option.EMPTY.value] == Value.GUARDS.value:
        for (chat_id, _) in guards.items():
            guards[chat_id].drop()
        
        await message.answer(text="Guards were #dropped.")
        return
    
    users_ids_list: List[int] = []
    
    if options[Option.EMPTY.value] == Value.ME.value:
        users_ids_list.append(Users.get(Users.telegram_id == message.chat.id))
    elif options[Option.EMPTY.value] == Value.ALL.value:
        users_ids_list = [ user.user_id for user in Users.select() ]
    elif options[Option.EMPTY.value] == Value.GROUPS.value:
        users_ids_list = [ group.user_id for group in GroupsOfStudents.select() ]
    elif options[Option.EMPTY.value] == Value.COMPACTS.value:
        users_ids_list = [ compact.user_id for compact in CompactStudents.select() ]
    elif options[Option.EMPTY.value] == Value.EXTENDEDS.value:
        users_ids_list = [ extended.user_id for extended in ExtendedStudents.select() ]
    elif options[Option.EMPTY.value] == Value.BBS.value:
        users_ids_list = [ bb.user_id for bb in BBStudents.select() ]
    else:
        await message.answer(text="The option has no matches!")
        return
    
    loading_message: Message = await message.answer(text="Started dropping…")
    progress_bar: str = ""
    
    for (index, user_id) in enumerate(users_ids_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values_number=len(users_ids_list), index=index
        )
        
        user: Users = Users.get(Users.user_id == user_id)
        
        try:
            if Option.MESSAGE.value in options:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=options[Option.MESSAGE.value],
                    parse_mode="markdown"
                )
            
            await message.bot.send_message(
                chat_id=user.telegram_id,
                text=(
                    "Текущие настройки сброшены!\n"
                    "Обнови данные — /login"
                )
            )
        except (CantInitiateConversation, UserDeactivated, BotBlocked, BotKicked, ChatNotFound):
            user.delete_instance()
        
        user.is_setup = False
        user.save()
    
    await loading_message.delete()
    
    await message.answer(text="{users_number} users were #dropped!".format(users_number=len(users_ids_list)))
