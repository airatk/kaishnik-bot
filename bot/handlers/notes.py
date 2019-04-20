from bot import kaishnik
from bot import students
from bot import metrics
from bot import on_callback_query

from bot.constants import NOTES_MAX_NUMBER

from bot.keyboards.notes import notes_chooser
from bot.keyboards.notes import notes_list_dailer

from bot.helpers import save_to
from bot.helpers import clarify_markdown

@kaishnik.message_handler(commands=["notes"])
def notes(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("notes")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[message.chat.id].notes),
            max=NOTES_MAX_NUMBER
        ),
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
        for note in students[callback.message.chat.id].notes:
            kaishnik.send_message(
                chat_id=callback.message.chat.id,
                text="{note}".format(note=note),
                parse_mode="Markdown"
            )

        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Заметок всего: *{current}/{max}*".format(
                current=len(students[callback.message.chat.id].notes),
                max=NOTES_MAX_NUMBER
            ),
            parse_mode="Markdown"
        )
    
    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: "show-note-" in callback.data)
def show_note(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    else:
        number = int(callback.data.replace("show-note-", ""))
        
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="{note}".format(note=students[callback.message.chat.id].notes[number]),
            parse_mode="Markdown"
        )

    on_callback_query(id=callback.id)

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "add-note")
def add_note_hint(callback):
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = len(students[callback.message.chat.id].notes) + 1
    
    if number > NOTES_MAX_NUMBER:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text="Лимит в {max} заметки уже достигнут.".format(max=NOTES_MAX_NUMBER)
        )
    else:
        kaishnik.send_message(
            chat_id=callback.message.chat.id,
            text=(
                "Добавляемая заметка будет *{number}* по счёту.\n\n"
                "• Используй звёздочки, чтобы выделить \**жирным*\*\n"
                "• Используй нижнее подчёркивание, чтобы выделить \__курсивом_\_\n\n"
                "Напиши заметку и отправь решительно.".format(number=number)
            ),
            parse_mode="Markdown"
        )
    
        students[callback.message.chat.id].previous_message = "/edit"

    on_callback_query(id=callback.id)

@kaishnik.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit")
def add_note(message):
    students[message.chat.id].previous_message = None
    students[message.chat.id].notes.append(clarify_markdown(message.text))
    
    save_to(filename="data/users", object=students)
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )

@kaishnik.callback_query_handler(func=lambda callback: "delete-note-" in callback.data)
def delete_note(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    else:
        number = int(callback.data.replace("delete-note-", ""))
        
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметка удалена! В ней было:\n\n{note}".format(note=students[callback.message.chat.id].notes[number]),
            parse_mode="Markdown"
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

@kaishnik.callback_query_handler(func=lambda callback: callback.data == "show-note" or callback.data == "delete-note")
def note_dailing(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    else:
        kaishnik.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выбери, какую заметку {action}:".format(action="показать" if "show" in callback.data else "удалить"),
            reply_markup=notes_list_dailer(
                notes=students[callback.message.chat.id].notes,
                action=callback.data
            )
        )

    on_callback_query(id=callback.id)
