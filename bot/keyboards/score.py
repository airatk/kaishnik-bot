from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

def semester_dailer(semesters_number):
    semester_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    semester_dailer_keyboard.add(*[
        InlineKeyboardButton(
            text=str(semester),
            callback_data="semester {}".format(semester)
        ) for semester in range(1, semesters_number)
    ])

    return semester_dailer_keyboard

def subject_chooser(scoretable, semester):
    subject_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    subject_chooser_keyboard.row(InlineKeyboardButton(
        text="Показать все",
        callback_data="scoretable all {n} {s}".format(n=len(scoretable), s=semester))
    )
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject[1][:len(subject[1]) - 6],  # (экз.) or (зач.) are 6 last charachters of a subject title
            callback_data="scoretable {n} {s}".format(n=int(subject[0]) - 1, s=semester)  # begin counting with 0, not with 1
        ) for subject in scoretable
    ])

    return subject_chooser_keyboard
