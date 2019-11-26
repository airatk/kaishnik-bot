from bot import bot
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


@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.CLEAR.value ]
)
def clear(message):
    loading_message = bot.send_message(
        chat_id=message.chat.id,
        text="Started clearing..."
    )
    
    is_cleared = False
    progress_bar = ""
    students_list = list(students)
    
    for (index, chat_id) in enumerate(students_list):
        progress_bar = update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=students_list, index=index
        )
        
        chat = bot.get_chat(chat_id=chat_id)
        
        try:
            bot.send_chat_action(chat_id=chat_id, action="typing")
        except Exception:
            bot.send_message(
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
                )
            )
            
            del students[chat_id]
            is_cleared = True
    
    save_data(file=USERS_FILE, object=students)
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Cleared!" if is_cleared else "No users to clear!"
    )

@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.ERASE.value ]
)
def erase(message):
    (option, _) = parse_creator_request(message.text)
    
    erase_list = []
    
    if option is None:
        bot.send_message(
            chat_id=message.chat.id,
            text="No option has been found!"
        )
        return
    elif option == EraseOption.ALL.value:
        erase_list = list(students)
    elif option == EraseOption.UNLOGIN.value:
        erase_list = [ chat_id for chat_id in list(students) if not students[chat_id].is_setup ]
    elif option == EraseOption.ME.value:
        erase_list = [ message.chat.id ]
    else:
        for possible_chat_id in message.text.split()[1:]:
            try:
                chat_id = int(possible_chat_id)
            except Exception:
                bot.send_message(
                    chat_id=message.chat.id,
                    text="*{invalid_chat_id}* cannot be a chat ID!".format(invalid_chat_id=possible_chat_id),
                    parse_mode="Markdown"
                )
            else:
                erase_list.append(chat_id)
    
    progress_bar = ""
    
    loading_message = bot.send_message(
        chat_id=message.chat.id,
        text="Started erasing…"
    )
    
    for (index, chat_id) in enumerate(erase_list):
        progress_bar = update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=erase_list, index=index
        )
        
        if chat_id in students:
            chat = bot.get_chat(chat_id=chat_id)
            
            bot.send_message(
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
                )
            )
            
            del students[chat_id]
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="{chat_id} doesn't use me!".format(chat_id=chat_id)
            )
    
    bot.send_message(
        chat_id=message.chat.id,
        text="No users to erase!" if len(erase_list) == 0 else "Erased!"
    )
    
    save_data(file=USERS_FILE, object=students)

@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DROP.value ]
)
def drop(message):
    (option, _) = parse_creator_request(message.text)
    
    drop_list = []
    
    if option == DropOption.ALL.value:
        drop_list = list(students)
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="If you are sure to drop all users' data, type */drop all*",
            parse_mode="Markdown"
        )
        return
    
    progress_bar = ""
    
    loading_message = bot.send_message(
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
                    bot.send_message(
                        chat_id=chat_id,
                        text=note,
                        parse_mode="Markdown",
                        disable_notification=True
                    )
                
                bot.send_message(
                    chat_id=chat_id,
                    text="Твои заметки, чтобы ничего не потерялось.",
                    disable_notification=True
                )
            
            students[chat_id] = Student()
            
            guard_message = bot.send_message(
                chat_id=chat_id,
                text="Текущие настройки сброшены.",
                disable_notification=True
            )
            bot.send_message(
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
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Data was #dropped!"
    )

@bot.message_handler(
    func=lambda message: message.chat.id == CREATOR,
    commands=[ Commands.GUARDDROP.value ]
)
def guarddrop(message):
    (option, _) = parse_creator_request(message.text)
    
    guarddrop_list = []
    
    if option is None:
        bot.send_message(
            chat_id=message.chat.id,
            text="No option has been found!"
        )
        return
    elif option == GuarddropOption.ALL.value:
        guarddrop_list = list(students)
    else:
        for possible_chat_id in message.text.split()[1:]:
            try:
                chat_id = int(possible_chat_id)
            except Exception:
                bot.send_message(
                    chat_id=message.chat.id,
                    text="*{invalid_chat_id}* cannot be a chat ID!".format(invalid_chat_id=possible_chat_id),
                    parse_mode="Markdown"
                )
            else:
                guarddrop_list.append(chat_id)
    
    for chat_id in guarddrop_list:
        if chat_id in students:
            students[chat_id].guard.drop()
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="{chat_id} doesn't use me!".format(chat_id=chat_id)
            )
    
    bot.send_message(
        chat_id=message.chat.id,
        text="No users to guarddrop!" if len(guarddrop_list) == 0 else "Guarddropped!"
    )
