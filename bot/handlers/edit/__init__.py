from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.edit import edit_chooser


@kbot.message_handler(
    commands=[ "edit" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("edit")
def edit(message):
    students[message.chat.id].previous_message = "/edit"  # Gate System (GS)
    
    edited_number = len(students[message.chat.id].edited_subjects)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "Изменить — это одновременно и изменить, и добавить."
            "\n\n"
            "Добавлено-изменено пар: *{}*".format(edited_number)
        ),
        reply_markup=edit_chooser(not_add_only=edited_number != 0),
        parse_mode="Markdown"
    )


# Importing respective edit menu options
from bot.handlers.edit import editoption
from bot.handlers.edit import showoption
from bot.handlers.edit import deleteoption


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message is not None and
        students[callback.message.chat.id].previous_message.startswith("/edit") and
        callback.data == "cancel-edit"
)
@top_notification
def cancel_edit(callback):
    students[callback.message.chat.id].edited_class = None
    
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="Отменено!"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/edit")
def gs_edit(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
