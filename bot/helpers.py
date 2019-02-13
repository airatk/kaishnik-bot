from constants import WEEK

from datetime import datetime
import pickle

# Set MSK timezone
import os, time; os.environ["TZ"] = "MSK"; time.tzset()

# No user data is lost anymore!
def save_users(users):
    with open("users.pkl", "wb") as users_file:
        pickle.dump(users, users_file, pickle.HIGHEST_PROTOCOL)

def load_users():
    with open("users.pkl", "rb") as users_file:
        return pickle.load(users_file)

# /week
def get_week():
    return "Текущая неделя чётная." if is_even() else "Текущая неделя нечётная."

def is_even():
    return not is_week_reversed() if datetime.today().isocalendar()[1] % 2 == 0 else is_week_reversed()

def is_week_reversed():
    with open("is_week_reversed", "r") as week_file:
        return True if week_file.read() == "True" else False

def reverse_week_in_file():
    with open("is_week_reversed", "w") as week_file:
        week_file.write("False") if is_week_reversed() else week_file.write("True")

# /classes
def beautify_classes(json_response, weekday, next):
    schedule = ""
    is_day_off = False
    
    for subject in json_response:
        # No subjects - no schedule. For day-offs
        is_day_off = "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]
        if is_day_off:
            break
    
        # Removing extraspaces
        for property in subject:
            subject[property] = " ".join(subject[property].split())
    
        # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
        if not next:
            if not is_even() and "чет" in subject["dayDate"] or is_even() and "неч" in subject["dayDate"]:
                continue
        else:
            if is_even() and "чет" in subject["dayDate"] or not is_even() and "неч" in subject["dayDate"]:
                continue
    
        # Make buildings look beautiful
        if subject["buildNum"] == "КАИ ОЛИМП":
            building = "СК Олимп"
        elif subject["buildNum"] == "1":
            building = "1ый дом"
        else:
            building = "".join([subject["buildNum"], "ка"])
    
        time_place = "\n\n*[ {time} ][ {building} ][ {auditorium} ]*".format(
            time=subject["dayTime"],
            building=building,
            auditorium=subject["audNum"] if subject["audNum"] else "-"
        )
        
        # Show if a subject is supposed to be only on certain date (like 21.09 or 07.11)
        date = "\n*[ Только {date} ]*".format(date=subject["dayDate"]) if "." in subject["dayDate"] else ""
        
        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        # Make subject types look beautiful
        if subject["disciplType"] == "лек":
            subject_type = "\n_лекция_"
        elif subject["disciplType"] == "пр":
            subject_type = "\n_практика_"
        elif subject["disciplType"] == "л.р.":
            subject_type = "\n_лабораторная работа_"
        else:
            subject_type = ""

        # Do not show empty strings
        teacher = "\n@ {teacher}".format(teacher=subject["prepodName"].title()) if subject["prepodName"] else ""
        department = "\n§  {department}".format(department=subject["orgUnitName"]) if subject["orgUnitName"] else ""
    
        # Concatenate all the stuff above
        schedule = "".join([schedule, time_place, date, subject_name, subject_type, teacher, department])
    
    return "".join([
        "*{weekday}*".format(weekday=WEEK[weekday]),
        schedule if schedule and not is_day_off else "\n\nВыходной"
    ])

# /exams
def beautify_exams(json_response):
    schedule = ""

    # Have no data to parse exams-json-response

    return schedule

# /score
def get_subject_score(score_table, subjects_num):
    subject = score_table[subjects_num]

    title = "*{title}*".format(title=subject[1][:len(subject[1]) - 6])

    if "экз" in subject[1]:
        type = "\n_экзамен_"
    else:
        type = "\n_зачёт_"

    certification1 = "\n\n• 1 аттестация: {gained}/{max}".format(gained=subject[2], max=subject[3])
    certification2 = "\n• 2 аттестация: {gained}/{max}".format(gained=subject[4], max=subject[5])
    certification3 = "\n• 3 аттестация: {gained}/{max}".format(gained=subject[6], max=subject[7])

    additional = "\n- Допбаллы: {gained}".format(gained=subject[9] if subject[9] else "-")
    debts = "\n- Долги: {gained}".format(gained=subject[10] if subject[10] else "-")

    preresult = "\n\nПредоценка: {preresult}".format(preresult=subject[8])
    result = "".join([
        "\nОценка: {mark}".format(mark=subject[12] if subject[12] != " " else "-"),
        " ({result})".format(result=subject[11]) if subject[11] != " " else ""
    ])

    return "".join([title, type, certification1, certification2, certification3, additional, debts, preresult, result])
