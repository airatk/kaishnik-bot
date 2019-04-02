from bot import kaishnik
from bot import students
from bot import metrics
from bot import on_callback_query

from bot.keyboards.notes import notes_chooser
from bot.keyboards.notes import notes_list_dailer

from bot.helpers import save_to

@kaishnik.message_handler(commands=["notes"])
def notes(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("notes")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Заметок всего: *{}/32*".format(len(students[message.chat.id].notes)),
        reply_markup=notes_chooser(),
        parse_mode="Markdown"
    )

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "show-all-notes")
def show_all_notes(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    if len(students[callback.message.chat.id].notes) == 0:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Заметок нет."
        )
    else:
        number = 0
        
        for note in students[callback.message.chat.id].notes:
            number += 1
            
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text=(
                    "Заметка №{number}\n\n"
                    "{note}".format(number=number, note=note)
                )
            )
    
    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: "show-note-" in callback.data)
def show_note(callback):
    number = int(callback.data.replace("show-note-", ""))
    
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "Заметка №{number}\n\n"
            "{note}".format(
                number=number + 1,
                note=students[callback.message.chat.id].notes[number]
            )
        )
    )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "add-note")
def add_note_hint(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = len(students[callback.message.chat.id].notes) + 1
    
    if number > 32:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Лимит в 32 заметки уже достигнут."
        )
    else:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text=(
                "Добавляемая заметка будет *{number}* по счёту.\n\n"
                "Напиши заметку и отправь решительно.".format(number=number)
            ),
            parse_mode="Markdown"
        )
    
        students[callback.message.chat.id].previous_message = "/edit"

    on_callback_query(id=callback.id)

@kaishnik.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit")
def add_note(message):
    students[message.chat.id].previous_message = None
    students[message.chat.id].notes.append(message.text)
    
    save_to(filename="data/users", object=students)
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )

@kaishnik.callback_query_handler(func=lambda callback: "delete-note-" in callback.data)
def delete_note(callback):
    number = int(callback.data.replace("delete-note-", ""))
    
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "Заметка №{number} удалена!\n"
            "В ней было:\n\n"
            "{note}\n\n".format(
                number=number + 1,
                note=students[callback.message.chat.id].notes[number]
            )
        )
    )
    
    del students[callback.message.chat.id].notes[number]
    
    save_to(filename="data/users", object=students)

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "delete-all-notes")
def delete_all_notes(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    else:
        students[callback.message.chat.id].notes = []
        
        save_to(filename="data/users", object=students)
        
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Удалено!"
        )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler( func=lambda callback: callback.data == "show-note" or callback.data == "delete-note")
def note_dailing(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет. Прям совсем."
        )
    else:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="{Action} заметку №".format(Action="Показать" if "show" in callback.data else "Удалить"),
            reply_markup=notes_list_dailer(
                notes_number=len(students[callback.message.chat.id].notes),
                action=callback.data
            )
        )

    on_callback_query(id=callback.id)
