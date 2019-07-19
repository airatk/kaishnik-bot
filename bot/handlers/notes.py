from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.notes import notes_chooser
from bot.keyboards.notes import notes_list_dialer

from bot.helpers           import save_to
from bot.helpers           import clarify_markdown
from bot.helpers.constants import MAX_NOTES_NUMBER


@kbot.message_handler(
    commands=["notes"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("notes")
def notes(message):
    students[message.chat.id].previous_message = "/notes"  # Gates System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Заметок всего: *{current}/{max}*".format(
            current=len(students[message.chat.id].notes),
            max=MAX_NOTES_NUMBER
        ),
        reply_markup=notes_chooser(len(students[message.chat.id].notes)),
        parse_mode="Markdown"
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "cancel-notes"
)
@top_notification
def cancel_edit(callback):
    students[callback.message.chat.id].edited_class = None
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отменено!"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "show-all-notes"
)
@top_notification
def show_all_notes(callback):
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
            max=MAX_NOTES_NUMBER
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        "show-note-" in callback.data
)
@top_notification
def show_note(callback):
    number = int(callback.data.replace("show-note-", ""))
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=students[callback.message.chat.id].notes[number],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "add-note"
)
@top_notification
def add_note_hint(callback):
    number = len(students[callback.message.chat.id].notes) + 1
    
    if number > MAX_NOTES_NUMBER:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="{max}-заметковый лимит уже достигнут.".format(max=MAX_NOTES_NUMBER)
        )
        
        students[callback.message.chat.id].previous_message = None  # Gates System (GS)
        return
    
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

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/notes add-new")
def add_note(message):
    students[message.chat.id].notes.append(clarify_markdown(message.text))
    students[message.chat.id].previous_message = None  # Gates System (GS)
    save_to(filename="data/users", object=students)
    
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        "delete-note-" in callback.data
)
@top_notification
def delete_note(callback):
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

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "delete-all-notes"
)
@top_notification
def delete_all_notes(callback):
    students[callback.message.chat.id].notes = []
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    save_to(filename="data/users", object=students)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Удалено!"
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/notes" and
        callback.data == "show-note" or callback.data == "delete-note"
)
@top_notification
def note_dailing(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери, какую заметку {action}:".format(action="показать" if "show" in callback.data else "удалить"),
        reply_markup=notes_list_dialer(
            notes=students[callback.message.chat.id].notes,
            action=callback.data
        )
    )


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/notes")
def gs_notes(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
