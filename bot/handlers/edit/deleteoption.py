from bot import kbot
from bot import students
from bot import top_notification

from bot.keyboards.edit.deleteoption import delete_edit_chooser

from bot.helpers import save_to


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        callback.data == "delete-edit"
)
@top_notification
def delete_edit(callback):
    edited_subjects = students[callback.message.chat.id].edited_subjects
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
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
    if "all" in callback.data:
        students[callback.message.chat.id].edited_subjects = []
    else:
        del students[callback.message.chat.id].edited_subjects[int(callback.data.replace("delete-edit-number-", ""))]
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
    save_to(filename="data/users", object=students)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Удалено!"
    )
