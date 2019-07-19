from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def semester_dialer(semesters_number):
    semester_dialer_keyboard = InlineKeyboardMarkup(row_width=2)
    
    semester_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=str(semester + 1),
            callback_data="semester {}".format(semester + 1)
        ) for semester in range(semesters_number)
    ])
    
    return semester_dialer_keyboard

def subject_chooser(scoretable, semester):
    subject_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    subject_chooser_keyboard.row(InlineKeyboardButton(
        text="Показать все",
        callback_data="scoretable all {n} {s}".format(n=len(scoretable), s=semester))
    )
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject[1].replace("(экз.)", "").replace("(зач.)", "").replace("(зач./оц.)", ""),
            callback_data="scoretable {n} {s}".format(n=int(subject[0]) - 1, s=semester)  # begin counting from 0, not from 1
        ) for subject in scoretable
    ])
    
    return subject_chooser_keyboard
