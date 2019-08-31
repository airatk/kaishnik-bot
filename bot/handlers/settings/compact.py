from bot import kbot
from bot import students
from bot import top_notification

from bot.helpers           import save_to
from bot.helpers.student   import Student
from bot.helpers.constants import GUIDE_MESSAGE

from re import fullmatch


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        callback.data == "settings-noncard-way"
)
@top_notification
def set_kit(callback):
    students[callback.message.chat.id] = Student(
        institute="-",
        institute_id="-",
        year="-",
        name="-",
        student_card_number="-"
    )
    
    students[callback.message.chat.id].previous_message = "/settings noncard-way"  # Gate System (GS)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отправь номер своей группы."
    )


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/settings noncard-way")
def set_kit_group_number(message):
    # Cleanning the chat
    kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try: kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception: pass
    
    students[message.chat.id].group_number = message.text

    if students[message.chat.id].group_number is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        return

    if students[message.chat.id].group_number == "non-existing":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Такой группы нет🤔"
        )
        kbot.send_message(
            chat_id=message.chat.id,
            text="Возможно, она появится позже, когда её внесут в каёвскую базу🤓"
        )
        kbot.send_message(
            chat_id=message.chat.id,
            text="Ещё разок? /settings"
        )

        students[message.chat.id] = Student()  # Drop all the entered data
        return

    students[message.chat.id].previous_message = None  # Gates System (GS)
    save_to(filename="data/users", object=students)

    kbot.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )
    kbot.send_message(
        chat_id=message.chat.id,
        text=GUIDE_MESSAGE,
        parse_mode="Markdown"
    )
