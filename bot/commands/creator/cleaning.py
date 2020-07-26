from aiogram.types import Message

from bot import dispatcher
from bot import students

from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.helpers import try_get_chat
from bot.commands.creator.utilities.helpers import get_user_data
from bot.commands.creator.utilities.helpers import collect_ids
from bot.commands.creator.utilities.constants import CREATOR

from bot.shared.api.student import Student
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.CLEAR.value ]
)
async def clear(message: Message):
    is_cleared: bool = False
    
    students_list: [int] = list(students)
    
    progress_bar: str = ""
    loading_message = await message.answer(text="Started clearing...")
    
    for (index, chat_id) in enumerate(students_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=students_list, index=index
        )
        
        (chat, error_text) = await try_get_chat(chat_id=chat_id)
        
        if chat is None:
            await message.answer(
                text="\n\n".join([ error_text, get_user_data(
                    student=students[chat_id],
                    hashtag="erased",
                    chat_id=chat_id
                ) ])
            )
            
            del students[chat_id]
            is_cleared = True
    
    await message.answer(text="Cleared!" if is_cleared else "No users to clear!")
    
    save_data(file=USERS_FILE, object=students)

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.ERASE.value ]
)
async def erase(message: Message):
    erase_list: [int] = await collect_ids(query_message=message)
    
    if len(erase_list) == len(students):
        students.clear()
        
        await message.answer(text="All users were #erased!")
        return
    
    progress_bar: str = ""
    loading_message: Message = await message.answer(text="Started erasing…")
    
    for (index, chat_id) in enumerate(erase_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=erase_list, index=index
        )
        
        if chat_id in students:
            (chat, error_text) = await try_get_chat(chat_id=chat_id)
            
            await message.answer(
                text="\n\n".join([ error_text, get_user_data(
                    student=students[chat_id],
                    hashtag="erased",
                    chat_id=chat_id, chat=chat
                ) ][1 if error_text is None else 0:])
            )
            
            del students[chat_id]
        else:
            await message.answer(text="*{chat_id}* doesn't use me!".format(chat_id=chat_id))
            
            erase_list.remove(chat_id)
    
    if len(erase_list) == 0:
        await loading_message.edit_text(text="No users to erase!")
    else:
        await message.answer(text="{users_number} users were #erased!".format(users_number=len(erase_list)))
        
        save_data(file=USERS_FILE, object=students)

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.DROP.value ]
)
async def drop(message: Message):
    drop_list: [int] = await collect_ids(query_message=message)
    
    progress_bar: str = ""
    loading_message: Message = await message.answer(text="Started dropping…")
    
    for (index, chat_id) in enumerate(drop_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=drop_list, index=index
        )
        
        try:
            if students[chat_id].notes != []:
                for note in students[chat_id].notes:
                    await message.bot.send_message(
                        chat_id=chat_id,
                        text=note,
                        parse_mode="markdown",
                        disable_notification=True
                    )
                
                await message.bot.send_message(
                    chat_id=chat_id,
                    text="Твои заметки, чтобы ничего не потерялось.",
                    disable_notification=True
                )
            
            students[chat_id]: Student = Student()
            
            await message.bot.send_message(
                chat_id=chat_id,
                text="Текущие настройки сброшены!",
                disable_notification=True
            )
            await message.bot.send_message(
                chat_id=chat_id,
                text="Обнови данные — /login",
                disable_notification=True
            )
        except ChatNotFound:
            del students[chat_id]
    
    if len(drop_list) == 0:
        await loading_message.edit_text(text="No users to drop!")
    else:
        await message.answer(text="Data was #dropped!")
        
        save_data(file=USERS_FILE, object=students)

@dispatcher.message_handler(
    lambda message: message.from_user.id == CREATOR,
    commands=[ Commands.GUARDDROP.value ]
)
async def guarddrop(message):
    guarddrop_list: [Student] = await collect_ids(query_message=message)
    
    for chat_id in guarddrop_list:
        if chat_id in students:
            students[chat_id].guard.drop()
        else:
            await message.answer(text="{chat_id} doesn't use me!".format(chat_id=chat_id))
            
            guarddrop_list.remove(chat_id)
    
    await message.answer(text="No users to guarddrop!" if len(guarddrop_list) == 0 else "Guarddropped!")
