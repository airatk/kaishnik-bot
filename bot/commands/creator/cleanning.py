from aiogram.types import Chat
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students

from bot.commands.creator.utilities.helpers import parse_creator_request
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import USER_DATA
from bot.commands.creator.utilities.types import EraseOption
from bot.commands.creator.utilities.types import DropOption
from bot.commands.creator.utilities.types import GuarddropOption

from bot.commands.start.utilities.keyboards import make_login

from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.CLEAR.value ]
)
async def clear(message: Message):
    is_cleared: bool = False
    progress_bar: str = ""
    students_list: [Student] = list(students)
    
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Started clearing..."
    )
    
    for (index, chat_id) in enumerate(students_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=students_list, index=index
        )
        
        chat: Chat = await bot.get_chat(chat_id=chat_id)
        
        try:
            await bot.send_chat_action(chat_id=chat_id, action="typing")
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text=USER_DATA.format(
                    firstname=chat.first_name, lastname=chat.last_name, username=chat.username,
                    chat_id=chat_id,
                    institute=students[chat_id].institute,
                    year=students[chat_id].year,
                    group_number=students[chat_id].group,
                    name=students[chat_id].name,
                    card=students[chat_id].card,
                    notes_number=len(students[chat_id].notes),
                    edited_classes_number=len(students[chat_id].edited_subjects),
                    fellow_students_number=len(students[chat_id].names),
                    is_full=students[chat_id].is_full,
                    guard_text=students[chat_id].guard.text,
                    is_guard_message_none=students[chat_id].guard.message is None,
                    hashtag="erased"
                ),
                parse_mode=None
            )
            
            del students[chat_id]
            is_cleared = True
    
    save_data(file=USERS_FILE, object=students)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Cleared!" if is_cleared else "No users to clear!"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.ERASE.value ]
)
async def erase(message: Message):
    (option, _) = parse_creator_request(message.text)
    
    erase_list: [Student] = []
    
    if option is None:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No option has been found!"
        )
        return
    elif option == EraseOption.ALL.value:
        erase_list = list(students)
    elif option == EraseOption.UNLOGIN.value:
        erase_list = [ chat_id for chat_id in list(students) if not students[chat_id].is_setup ]
    elif option == EraseOption.ME.value:
        erase_list.append(message.chat.id)
    else:
        for possible_chat_id in message.text.split()[1:]:
            try:
                chat_id: int = int(possible_chat_id)
            except Exception:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="*{invalid_chat_id}* cannot be a chat ID!".format(invalid_chat_id=possible_chat_id)
                )
            else:
                erase_list.append(chat_id)
    
    progress_bar: str = ""
    
    loading_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text="Started erasing…"
    )
    
    for (index, chat_id) in enumerate(erase_list):
        progress_bar = update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=erase_list, index=index
        )
        
        if chat_id in students:
            chat: Chat = await bot.get_chat(chat_id=chat_id)
            
            await bot.send_message(
                chat_id=message.chat.id,
                text=USER_DATA.format(
                    firstname=chat.first_name, lastname=chat.last_name, username=chat.username,
                    chat_id=chat_id,
                    institute=students[chat_id].institute,
                    year=students[chat_id].year,
                    group_number=students[chat_id].group,
                    name=students[chat_id].name,
                    card=students[chat_id].card,
                    notes_number=len(students[chat_id].notes),
                    edited_classes_number=len(students[chat_id].edited_subjects),
                    fellow_students_number=len(students[chat_id].names),
                    is_full=students[chat_id].is_full,
                    guard_text=students[chat_id].guard.text,
                    is_guard_message_none=students[chat_id].guard.message is None,
                    hashtag="erased"
                ),
                parse_mode=None
            )
            
            del students[chat_id]
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="{chat_id} doesn't use me!".format(chat_id=chat_id)
            )
            
            erase_list.remove(chat_id)
    
    if len(erase_list) == 0:
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="No users to erase!" if len(erase_list) == 0 else "Erased!"
    )
    
    save_data(file=USERS_FILE, object=students)

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DROP.value ]
)
async def drop(message: Message):
    (option, _) = parse_creator_request(message.text)
    
    drop_list: [Student] = []
    
    if option == DropOption.ALL.value:
        drop_list = list(students)
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to drop all users' data, type */drop all*"
        )
        return
    
    progress_bar: str = ""
    
    loading_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text="Started dropping…"
    )
    
    for (index, chat_id) in enumerate(drop_list):
        progress_bar = update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=drop_list, index=index
        )
        
        try:
            if students[chat_id].notes != []:
                for note in students[chat_id].notes:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=note,
                        disable_notification=True
                    )
                
                await bot.send_message(
                    chat_id=chat_id,
                    text="Твои заметки, чтобы ничего не потерялось.",
                    disable_notification=True
                )
            
            students[chat_id]: Student = Student()
            
            guard_message: Message = await bot.send_message(
                chat_id=chat_id,
                text="Текущие настройки сброшены.",
                disable_notification=True
            )
            await bot.send_message(
                chat_id=chat_id,
                text="Обнови данные:",
                reply_markup=make_login(),
                disable_notification=True
            )
            
            students[message.chat.id].guard.text = Commands.START.value
            students[chat_id].guard.message = guard_message
        except Exception:
            del students[chat_id]
    
    save_data(file=USERS_FILE, object=students)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Data was #dropped!"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.GUARDDROP.value ]
)
async def guarddrop(message):
    (option, _) = parse_creator_request(message.text)
    
    guarddrop_list: [Student] = []
    
    if option is None:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No option has been found!"
        )
        return
    elif option == GuarddropOption.ALL.value:
        guarddrop_list = list(students)
    else:
        for possible_chat_id in message.text.split()[1:]:
            try:
                chat_id: int = int(possible_chat_id)
            except Exception:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="*{invalid_chat_id}* cannot be a chat ID!".format(invalid_chat_id=possible_chat_id)
                )
            else:
                guarddrop_list.append(chat_id)
    
    for chat_id in guarddrop_list:
        if chat_id in students:
            students[chat_id].guard.drop()
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="{chat_id} doesn't use me!".format(chat_id=chat_id)
            )
            
            guarddrop_list.remove(chat_id)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="No users to guarddrop!" if len(guarddrop_list) == 0 else "Guarddropped!"
    )
