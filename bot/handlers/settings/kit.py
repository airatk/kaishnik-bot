from bot import kbot
from bot import students
from bot import top_notification

from bot.helpers           import save_to
from bot.helpers.student   import Student
from bot.helpers.constants import REPLIES_TO_UNKNOWN_COMMAND

from re import fullmatch


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        callback.data == "set-institute-КИТ"
)
@top_notification
def set_kit(callback):
    students[callback.message.chat.id] = Student(
        institute="КИТ",
        institute_id="КИТ",
        year="unknown",
        name="unknown",
        student_card_number="unknown"
    )
    
    students[callback.message.chat.id].previous_message = "/settings set-kit-group"  # Gate System (GS)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер своей группы."
    )


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/settings set-kit-group")
def set_kit_group_number(message):
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass
    
    if fullmatch("[4][1-4][2-5][0-9]", message.text):
        students[message.chat.id].group_number = message.text
    
        if students[message.chat.id].group_number is None:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Сайт kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
            
            students[message.chat.id] = Student()  # Drop all the entered data
        elif students[message.chat.id].group_number != "non-existing":
            students[message.chat.id].previous_message = None  # Gates System (GS)
            save_to(filename="data/users", object=students)
            
            kbot.send_message(
                chat_id=message.chat.id,
                text="Запомнено!"
            )
            kbot.send_message(
                chat_id=message.chat.id,
                text=REPLIES_TO_UNKNOWN_COMMAND[0],
                parse_mode="Markdown"
            )
        else:
            kbot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Такой группы не существует🤔"
            )

            students[callback.message.chat.id] = Student()  # Drop all the entered data
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Неверный номер группы. Исправляйся."
        )