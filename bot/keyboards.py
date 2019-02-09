from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardRemove

from constants import buildings
from constants import libraries
from constants import dorms
from constants import institutes
from helpers   import get_dict_of_list
from helpers   import get_score_table

# /start
def settings_entry():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton(text="/settings"))

# /classes
def schedule_type():
    schedule_type_keyboard = InlineKeyboardMarkup()

    schedule_type_keyboard.row(
        InlineKeyboardButton(text="сегодня", callback_data="today's"),
        InlineKeyboardButton(text="завтра", callback_data="tomorrow's")
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю", callback_data="weekly current"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю", callback_data="weekly next"))

    return schedule_type_keyboard

# /score
def semester_dailer():
    from student import student

    semester_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    semesters_number = int(student.get_year())*2 + 1
    
    semester_dailer_keyboard.add(*[
        InlineKeyboardButton(text=str(s_r), callback_data="s_r {s_r}".format(s_r=s_r)) for s_r in range(1, semesters_number)
    ])

    return semester_dailer_keyboard

def subject_chooser(semester):
    subject_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    score_table = get_score_table(semester)
    
    subject_chooser_keyboard.add(InlineKeyboardButton(
        text="Показать все",
        callback_data="s_t all {n} {s}".format(n=len(score_table), s=semester))
    )
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject[1][:len(subject[1]) - 6],
            callback_data="s_t {n} {s}".format(n=int(subject[0]) - 1, s=semester)
        ) for subject in score_table
    ])

    return subject_chooser_keyboard

# /locations
def choose_location_type():
    location_type_keyboard = InlineKeyboardMarkup()

    location_type_keyboard.row(InlineKeyboardButton(text="Учебные здания и СК", callback_data="buildings"))
    location_type_keyboard.row(InlineKeyboardButton(text="Библиотеки", callback_data="libraries"))
    location_type_keyboard.row(InlineKeyboardButton(text="Общежития", callback_data="dorms"))

    return location_type_keyboard

def buildings_dailer():
    buildings_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dailer_keyboard.add(*[
        InlineKeyboardButton(text=b_, callback_data="b_s {b_}".format(b_=b_)) for b_ in buildings
    ])

    return buildings_dailer_keyboard

def libraries_dailer():
    libraries_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dailer_keyboard.add(*[
        InlineKeyboardButton(text=l_, callback_data="l_s {l_}".format(l_=l_)) for l_ in libraries
    ])

    return libraries_dailer_keyboard

def dorms_dailer():
    dorms_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dailer_keyboard.add(*[
        InlineKeyboardButton(text=d_, callback_data="d_s {d_}".format(d_=d_)) for d_ in dorms
    ])

    return dorms_dailer_keyboard

# /settings
def institute_setter():
    institute_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    institute_setter_keyboard.add(*[
        KeyboardButton(text=institute) for institute in institutes
    ])

    return institute_setter_keyboard

def year_setter():
    from student import student

    year_setter_keyboard = ReplyKeyboardMarkup(row_width=6, resize_keyboard=True)

    params = (
        ("p_fac", student.get_institute()),
    )

    year_setter_keyboard.add(*[
        KeyboardButton(text=year) for year in get_dict_of_list(type="p_kurs", params=params)
    ])

    return year_setter_keyboard

def group_number_setter():
    from student import student

    group_number_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    params = (
        ("p_fac", student.get_institute()),
        ("p_kurs", student.get_year())
    )

    group_number_setter_keyboard.add(*[
        KeyboardButton(text=group) for group in get_dict_of_list(type="p_group", params=params)
    ])

    return group_number_setter_keyboard

def name_setter():
    from student import student

    name_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    params = (
        ("p_fac", student.get_institute()),
        ("p_kurs", student.get_year()),
        ("p_group", student.get_group_number_for_score())
    )

    name_setter_keyboard.add(*[
        KeyboardButton(text=name) for name in get_dict_of_list(type="p_stud", params=params)
    ])

    return name_setter_keyboard

# Remove keyboard
def remove_keyboard():
    return ReplyKeyboardRemove()
