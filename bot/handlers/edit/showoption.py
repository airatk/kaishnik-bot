from bot import kbot
from bot import students
from bot import top_notification

from bot.keyboards.edit.showoption import edited_classes_weektype_dialer
from bot.keyboards.edit.showoption import edited_classes_weekday_dialer
from bot.keyboards.edit.showoption import edited_classes_one_dialer

from bot.helpers.constants import WEEKDAYS


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        callback.data == "show-edit"
)
@top_notification
def show_edit(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "В скобках указано количество отредактированных пар в соответствующую неделю.\n\n"
            "Выбери тип недели:"
        ),
        reply_markup=edited_classes_weektype_dialer(students[callback.message.chat.id].edited_subjects)
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "show-all-edit-" in callback.data
)
@top_notification
def show_all_edit(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    callback_data = callback.data.replace("show-all-edit-", "").split("-")
    
    weektypes = { "каждая": None, "чётная": True, "нечётная": False }
    weekdays = WEEKDAYS
    
    # weektypes
    if callback_data[0] != "all":
        if callback_data[0] == "even": weektypes = { "чётная": True }
        elif callback_data[0] == "odd": weektypes = { "нечётная": False }
        elif callback_data[0] == "none": weektypes = { "каждая": None }
    
        # weekdays
        if callback_data[1] != "all": weekdays = { int(callback_data[1]): WEEKDAYS[int(callback_data[1])] }
    
    subjects_num = 0
    
    for weektype, is_even in weektypes.items():
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="*{} неделя*".format(weektype),
            parse_mode="Markdown"
        )
        
        for weekday, weekday_name in weekdays.items():
            message = "*{}*".format(weekday_name)
            has_edited = False
            
            for edited_class in students[callback.message.chat.id].edited_subjects:
                if edited_class.weekday == weekday and edited_class.is_even == is_even:
                    message = "".join([ message, edited_class.get() ])
                    subjects_num += 1
                    has_edited = True
        
            if has_edited:
                kbot.send_message(
                    chat_id=callback.message.chat.id,
                    text=message,
                    parse_mode="Markdown"
                )

    if subjects_num == 1: grammatical_entity = "а"
    elif subjects_num in range(2, 5): grammatical_entity = "ы"
    else: grammatical_entity = ""

    kbot.send_message(
        chat_id=callback.message.chat.id,
        text="*{}* пар{} всего!".format(subjects_num, grammatical_entity),
        parse_mode="Markdown"
    )

    students[callback.message.chat.id].previous_message = None  # Gate System (GS)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "show-weektype-" in callback.data
)
@top_notification
def show_weekday_edit(callback):
    weektype = callback.data.replace("show-weektype-", "")
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери день:",
        reply_markup=edited_classes_weekday_dialer(weektype, students[callback.message.chat.id].edited_subjects)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "show-weekday-" in callback.data
)
@top_notification
def show_weekday_edit(callback):
    callback_data = callback.data.replace("show-weekday-", "").split("-")
    weekday = int(callback_data[0])
    weektype = callback_data[1]
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери пару:",
        reply_markup=edited_classes_one_dialer(weektype, weekday, students[callback.message.chat.id].edited_subjects)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/edit" and
        "show-one-" in callback.data
)
@top_notification
def show_one_edit(callback):
    subject = students[callback.message.chat.id].edited_subjects[int(callback.data.replace("show-one-", ""))]
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=subject.get(),
        parse_mode="Markdown"
    )

    students[callback.message.chat.id].previous_message = None  # Gate System (GS)
