from bot import kbot
from bot import students
from bot import metrics
from bot import hide_loading_notification

from bot.constants import NOTES_MAX_NUMBER

from bot.keyboards.notes import notes_chooser
from bot.keyboards.notes import notes_list_dialer

from bot.helpers import save_to
from bot.helpers import clarify_markdown


@kbot.message_handler(
    commands=["notes"],
    func=lambda message: students[message.chat.id].previous_message is None
)
def notes(message):
    metrics.increment("notes")
    
    students[message.chat.id].previous_message = "/notes"  # Gates System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[message.chat.id].notes),
            max=NOTES_MAX_NUMBER
        ),
        reply_markup=notes_chooser(),
        parse_mode="Markdown"
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "show-all-notes"
)
def show_all_notes(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    else:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        for note in students[callback.message.chat.id].notes:
            kbot.send_message(
                chat_id=callback.message.chat.id,
                text=note,
                parse_mode="Markdown"
            )
        
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="Заметок всего: *{current}/{max}*".format(
                current=len(students[callback.message.chat.id].notes),
                max=NOTES_MAX_NUMBER
            ),
            parse_mode="Markdown"
        )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        "show-note-" in callback.data
)
def show_note(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    else:
        number = int(callback.data.replace("show-note-", ""))
        
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=students[callback.message.chat.id].notes[number],
            parse_mode="Markdown"
        )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    
    hide_loading_notification(id=callback.id)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "add-note"
)
def add_note_hint(callback):
    number = len(students[callback.message.chat.id].notes) + 1
    
    if number > NOTES_MAX_NUMBER:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="{max}-заметковый лимит уже достигнут.".format(max=NOTES_MAX_NUMBER)
        )
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=(
                "Добавляемая заметка будет *{number}* по счёту.\n\n"
                "• Используй звёздочки, чтобы выделить \**жирным*\*\n"
                "• Используй нижнее подчёркивание, чтобы выделить \__курсивом_\_\n\n"
                "Напиши заметку и отправь решительно.".format(number=number)
            ),
            parse_mode="Markdown"
        )
        
        students[callback.message.chat.id].previous_message = "/notes add-new"

    hide_loading_notification(id=callback.id)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/notes add-new")
def add_note(message):
    students[message.chat.id].notes.append(clarify_markdown(message.text))
    
    students[message.chat.id].previous_message = None  # Gates System (GS)
    
    save_to(filename="data/users", object=students)
    
    # Cleanning the chat
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        "delete-note-" in callback.data
)
def delete_note(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    
        students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    else:
        number = int(callback.data.replace("delete-note-", ""))
        
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=(
                "Заметка удалена!\n"
                "В ней было:\n\n"
                "{note}".format(note=students[callback.message.chat.id].notes[number])
            ),
            parse_mode="Markdown"
        )
        
        del students[callback.message.chat.id].notes[number]
        
        students[callback.message.chat.id].previous_message = None  # Gates System (GS)
        
        save_to(filename="data/users", object=students)
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "delete-all-notes"
)
def delete_all_notes(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    
        students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    else:
        students[callback.message.chat.id].notes = []
        
        students[callback.message.chat.id].previous_message = None  # Gates System (GS)
        
        save_to(filename="data/users", object=students)
        
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Удалено!"
        )

    hide_loading_notification(id=callback.id)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "show-note" or callback.data == "delete-note"
)
def note_dailing(callback):
    if len(students[callback.message.chat.id].notes) == 0:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Заметок нет."
        )
    
        students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    else:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выбери, какую заметку {action}:".format(action="показать" if "show" in callback.data else "удалить"),
            reply_markup=notes_list_dialer(
                notes=students[callback.message.chat.id].notes,
                action=callback.data
            )
        )

    hide_loading_notification(id=callback.id)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/notes")
def gs_notes(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
