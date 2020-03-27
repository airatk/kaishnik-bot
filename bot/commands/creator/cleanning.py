from aiogram.types import Chat
from aiogram.types import Message
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.exceptions import Unauthorized

from bot import dispatcher
from bot import students

from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.helpers import get_user_data
from bot.commands.creator.utilities.helpers import collect_ids
from bot.commands.creator.utilities.constants import CREATOR

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
    
    students_list: [int] = list(students)
    
    progress_bar: str = ""
    loading_message = await message.answer(text="Started clearing...")
    
    for (index, chat_id) in enumerate(students_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=students_list, index=index
        )
        
        try:
            chat: Chat = await message.bot.get_chat(chat_id=chat_id)
            await message.bot.send_chat_action(chat_id=chat_id, action="typing")
        except ChatNotFound:
            await message.answer(text=get_user_data(chat=chat, student=students[chat_id], hashtag="erased"))
            
            del students[chat_id]
            is_cleared = True
        except Unauthorized:
            await message.answer(text="Troubles getting the {chat_id} chat, but it was #erased.".format(chat_id=chat_id))
            
            del students[chat_id]
            is_cleared = True
    
    save_data(file=USERS_FILE, object=students)
    
    await message.answer(text="Cleared!" if is_cleared else "No users to clear!")

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.ERASE.value ]
)
async def erase(message: Message):
    erase_list: [int] = await collect_ids(query_message=message)
    
    progress_bar: str = ""
    loading_message: Message = await message.answer(text="Started erasing…")
    
    for (index, chat_id) in enumerate(erase_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=erase_list, index=index
        )
        
        if chat_id in students:
            try:
                chat: Chat = await message.bot.get_chat(chat_id=chat_id)
            except (ChatNotFound, Unauthorized):
                await message.answer(text="Troubles getting the chat, but the chat id was #erased.")
            else:
                await message.answer(text=get_user_data(chat=chat, student=students[chat_id], hashtag="erased"))
            
            del students[chat_id]
        else:
            await message.answer(text="*{chat_id}* doesn't use me!".format(chat_id=chat_id))
            
            erase_list.remove(chat_id)
    
    if len(erase_list) == 0: await loading_message.delete()
    
    await message.answer(text="No users to erase!" if len(erase_list) == 0 else "Erased!")
    
    save_data(file=USERS_FILE, object=students)

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DROP.value ]
)
async def drop(message: Message):
    drop_list: [int] = await collect_ids(query_message=message)
    
    progress_bar: str = ""
    loading_message: Message = await message.answer(text="Started dropping…")
    
    for (index, chat_id) in enumerate(drop_list):
        progress_bar = update_progress_bar(
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
            
            guard_message: Message = await message.bot.send_message(
                chat_id=chat_id,
                text="Текущие настройки сброшены!",
                disable_notification=True
            )
            await message.bot.send_message(
                chat_id=chat_id,
                text="Обнови данные:",
                reply_markup=make_login(),
                disable_notification=True
            )
            
            students[message.chat.id].guard.text = Commands.START.value
            students[chat_id].guard.message = guard_message
        except ChatNotFound:
            del students[chat_id]
    
    save_data(file=USERS_FILE, object=students)
    
    await message.answer(text="Data was #dropped!")

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
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
