from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.keyboards.settings import institute_setter

from bot.helpers.student import Student


@kbot.callback_query_handler(func=lambda callback: callback.data == "first-setup")
@top_notification
def first_setup(callback):
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    except Exception:
        pass
    
    settings(callback.message)


@kbot.message_handler(
    commands=["settings"],
    func=lambda message:
        students[message.chat.id].previous_message == "/start" or
        students[message.chat.id].previous_message is None
)
@metrics.increment("settings")
def settings(message):
    students[message.chat.id].previous_message = "/settings"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="{warning}Выбери своё подразделение:".format(
            # Show the warning to the old users
            warning=(
                "Все текущие данные, включая "
                "*заметки*, *изменённое расписание* и *номер зачётки*, "
                "будут стёрты.\n\n"
            ) if not students[message.chat.id].is_not_set_up() else ""
        ),
        reply_markup=institute_setter(is_old=not students[message.chat.id].is_not_set_up()),
        parse_mode="Markdown"
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message is not None and
        students[callback.message.chat.id].previous_message.startswith("/settings") and
        callback.data == "cancel-settings"
)
@top_notification
def cancel_setting_process(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Отменено!"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


# Importing respective settings menus
from bot.handlers.settings import institutes
from bot.handlers.settings import kit


@kbot.message_handler(
    func=lambda message:
        students[message.chat.id].previous_message is not None and
        students[message.chat.id].previous_message.startswith("/settings")
)
def gs_settings(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@kbot.callback_query_handler(func=lambda callback: students[callback.message.chat.id].is_not_set_up())
@top_notification
def deny_access_to_unsetup_callback(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    deny_access_to_unsetup_message(callback.message)

@kbot.message_handler(func=lambda message: students[message.chat.id].is_not_set_up())
@metrics.increment("unsetup")
def deny_access_to_unsetup_message(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "Настройка пройдена не полностью, исправляйся —\n"
            "/settings"
        )
    )
