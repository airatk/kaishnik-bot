from bot import kbot
from bot import students
from bot import metrics

from bot.keyboards.settings import set_card_skipper

from bot.helpers           import is_even
from bot.helpers           import weekday_date
from bot.helpers.constants import BRS
from bot.helpers.constants import HELP
from bot.helpers.constants import DONATE


@kbot.message_handler(
    commands=[ "week" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("week")
def week(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=(
            "{weekday}, {date}. \n"
            "Текущая неделя *{type}*.".format(
                weekday=weekday_date()["weekday"],
                date=weekday_date()["date"],
                type="чётная" if is_even() else "нечётная"
            )
        ),
        parse_mode="Markdown"
    )


@kbot.message_handler(
    commands=[ "card" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("card")
def card(message):
    if students[message.chat.id].institute_id == "КИТ":
        kbot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
        return
    
    if students[message.chat.id].student_card_number == "unset":
        kbot.send_message(
            chat_id=message.chat.id,
            text=(
                "Отправь номер своей зачётки "
                "(интересный факт — студенческий билет и зачётка имеют одинаковый номер!)."
                "\n\n"
                "Либо пропусти, но баллы показать не смогу."
            ),
            reply_markup=set_card_skipper()
        )
        
        students[message.chat.id].student_card_number = None
        students[message.chat.id].previous_message = "/settings student-card-number"  # Gate System (GS)
        return

    kbot.send_message(
        chat_id=message.chat.id,
        text="Номер твоего студенческого билета и твоей зачётной книжки: *{card}*".format(
            card=students[message.chat.id].student_card_number
        ),
        parse_mode="Markdown"
    )


@kbot.message_handler(
    commands=[ "brs" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("brs")
def brs(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=BRS,
        parse_mode="Markdown"
    )


@kbot.message_handler(
    commands=[ "help" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("help")
def help(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=HELP,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


@kbot.message_handler(
    commands=[ "donate" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("donate")
def donate(message):
    kbot.send_message(
        chat_id=message.chat.id,
        text=DONATE,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


@kbot.message_handler(
    commands=[ "me" ],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("me")
def me(message):
    chat = kbot.get_chat(chat_id=message.chat.id)
    
    if students[message.chat.id].institute_id == "КИТ":
        message_text = (
            "{firstname}{lastname}{username}\n"
            "chat id {chat_id}\n"
            "\n"
            "• Колледж: {institute}\n"
            "• Группа: {group_number}\n"
            "\n"
            "• Заметок: {notes_number}\n"
            "• Изменений в расписании: {edited_classes_number}".format(
                firstname=chat.first_name,
                lastname=f" {chat.last_name}" if chat.last_name is not None else "",
                username=f" @{chat.username}" if chat.username is not None else "",
                chat_id=message.chat.id,
                institute=students[message.chat.id].institute,
                group_number=students[message.chat.id].group_number,
                notes_number=len(students[message.chat.id].notes),
                edited_classes_number=len(students[message.chat.id].edited_subjects)
            )
        )
    else:
        message_text = (
            "{firstname}{lastname}{username}\n"
            "chat id {chat_id}\n"
            "\n"
            "• Институт: {institute}\n"
            "• Курс: {year}\n"
            "• Группа: {group_number}\n"
            "• Имя: {name}\n"
            "• Номер зачётки: {card}\n"
            "\n"
            "• Заметок: {notes_number}\n"
            "• Изменений в расписании: {edited_classes_number}".format(
                firstname=chat.first_name,
                lastname=f" {chat.last_name}" if chat.last_name is not None else "",
                username=f" @{chat.username}" if chat.username is not None else "",
                chat_id=message.chat.id,
                institute=students[message.chat.id].institute,
                year=students[message.chat.id].year,
                group_number=students[message.chat.id].group_number,
                name=students[message.chat.id].name,
                card=students[message.chat.id].student_card_number,
                notes_number=len(students[message.chat.id].notes),
                edited_classes_number=len(students[message.chat.id].edited_subjects)
            )
        )
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=message_text
    )
