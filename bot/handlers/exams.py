from bot import kbot
from bot import students
from bot import metrics

from re import fullmatch


@kbot.message_handler(
    commands=["exams"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("exams")
def exams(message):
    another_group = message.text.replace("/exams", "")
    
    if another_group != "":
        another_group = another_group[1:]  # Getting rid of a whitespace
        
        if fullmatch("[1-59][1-6][0-9][0-9]", another_group):
            kbot.send_message(
                chat_id=message.chat.id,
                text="Неверный номер группы. Исправляйся."
            )
            
            students[message.chat.id].previous_message = None  # Gate System (GS)
            return
        
        students[message.chat.id].another_group_number_schedule = another_group
    
        if students[message.chat.id].another_group_number_schedule is None:
            kbot.send_message(
                chat_id=message.chat.id,
                text="kai.ru не отвечает🤷🏼‍♀️",
                disable_web_page_preview=True
            )
            
            students[message.chat.id].previous_message = None  # Gate System (GS)
            return
    
    kbot.send_message(
        chat_id=message.chat.id,
        text=students[message.chat.id].get_schedule(type="exams")[0],
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    students[message.chat.id].another_group_number_schedule = None
