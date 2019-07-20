from bot import kbot
from bot import students
from bot import top_notification

from bot.keyboards.edit.delete import delete_edit_chooser

from bot.helpers import save_to


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        callback.data == "delete-edit"
)
@top_notification
def delete_edit(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    edited_subjects = students[callback.message.chat.id].edited_subjects
    
    if edited_subjects == []:
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="Добавленных пар нет."
        )

        students[callback.message.chat.id].previous_message = None  # Gate System (GS)
        return
    
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="Выбери пару, которую нужно удалить:",
        reply_markup=delete_edit_chooser(edited_subjects)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "delete-edit-" in callback.data
)
@top_notification
def delete_edited(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    if "all" in callback.data:
        students[callback.message.chat.id].edited_subjects = []
    else:
        del students[callback.message.chat.id].edited_subjects[int(callback.data.replace("delete-edit-number-", ""))]
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
    save_to(filename="data/users", object=students)
    
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="Удалено!"
    )
