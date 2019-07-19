from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import MONTHS

from datetime import datetime

from pickle import load
from pickle import dump
from pickle import HIGHEST_PROTOCOL


# Saving & loading data functions
def save_to(filename, object):
    with open(filename, "wb") as file:
        dump(object, file, HIGHEST_PROTOCOL)

def load_from(filename):
    with open(filename, "rb") as file:
        return load(file)


# /week
def is_even():
    return not is_week_reversed() if datetime.today().isocalendar()[1] % 2 == 0 else is_week_reversed()

def is_week_reversed():
    return load_from("data/is_week_reversed")

def weekday_date():
    date = datetime.today()
    weekday = date.isoweekday()
    
    return {
        "weekday": WEEKDAYS[weekday] if weekday != 7 else "Воскресенье",
        "date": "{day} {month}".format(
            day=int(date.strftime("%d")),
            month=MONTHS[date.strftime("%m")]
            # This str(int(:string:)) was done to replace "01 апреля" by "1 апреля"
        )
    }


# /score
def get_subject_score(scoretable, subjects_num):
    subject = scoretable[subjects_num]
    
    title = "*{title}*".format(title=subject[1].replace("(экз.)", "").replace("(зач.)", "").replace("(зач./оц.)", ""))
    
    if "(экз.)" in subject[1]:
        type = "\n_экзамен_\n"
    elif "(зач.)" in subject[1]:
        type = "\n_зачёт_\n"
    elif "(зач./оц.)" in subject[1]:
        type = "\n_зачёт с оценкой_\n"
    
    certification1 = "\n• 1 аттестация: {gained} / {max}".format(gained=subject[2], max=subject[3])
    certification2 = "\n• 2 аттестация: {gained} / {max}".format(gained=subject[4], max=subject[5])
    certification3 = "\n• 3 аттестация: {gained} / {max}".format(gained=subject[6], max=subject[7])
    semesterSum = "\n◦ За семестр: {}".format(subject[8])
    
    debts = "\n\nДолги: {}".format(subject[10])
    
    return "".join([ title, type, certification1, certification2, certification3, semesterSum, debts ])


# /notes
def clarify_markdown(string):
    is_single = False
    
    for index, letter in enumerate(string):
        if letter in [ "*", "_" ]:
            index = index
            is_single = not is_single
    
    return "".join([string[:index], "\\", string[index:]]) if is_single else string
