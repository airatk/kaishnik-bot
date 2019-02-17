from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)

from constants import (
    INSTITUTES,
    BUILDINGS, LIBRARIES, DORMS
)

# /start
def settings_entry():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton(text="/settings"))

# /settings
def institute_setter():
    institute_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    institute_setter_keyboard.add(*[
        KeyboardButton(text=institute) for institute in INSTITUTES
    ])

    return institute_setter_keyboard

def year_setter(years):
    year_setter_keyboard = ReplyKeyboardMarkup(row_width=6, resize_keyboard=True)

    year_setter_keyboard.add(*[
        KeyboardButton(text=year) for year in years
    ])

    return year_setter_keyboard

def group_number_setter(groups):
    group_number_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    group_number_setter_keyboard.add(*[
        KeyboardButton(text=group) for group in groups
    ])

    return group_number_setter_keyboard

def name_setter(names):
    name_setter_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    name_setter_keyboard.add(*[
        KeyboardButton(text=name) for name in names
    ])

    return name_setter_keyboard

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

# /lecturers
def choose_lecturer(names):
    choose_lecturer_keyboard = InlineKeyboardMarkup(row_width=1)

    choose_lecturer_keyboard.add(*[
        InlineKeyboardButton(text=name["lecturer"], callback_data="l_r " + name["id"]) for name in names
    ])

    return choose_lecturer_keyboard

def lecturer_schedule_type(prepod_login):
    lecturer_schedule_type_keyboard = InlineKeyboardMarkup()

    lecturer_schedule_type_keyboard.row(InlineKeyboardButton(text="занятий", callback_data=" ".join(["l_c", prepod_login])))
    lecturer_schedule_type_keyboard.row(InlineKeyboardButton(text="экзаменов", callback_data=" ".join(["l_e", prepod_login])))

    return lecturer_schedule_type_keyboard

# /score
def semester_dailer(semesters_number):
    semester_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    semester_dailer_keyboard.add(*[
        InlineKeyboardButton(text=str(s_r), callback_data="s_r {s_r}".format(s_r=s_r)) for s_r in range(1, semesters_number)
    ])

    return semester_dailer_keyboard

def subject_chooser(score_table, semester):
    subject_chooser_keyboard = InlineKeyboardMarkup(row_width=1)
    
    subject_chooser_keyboard.add(InlineKeyboardButton(
        text="Показать все",
        callback_data="s_t all {n} {s}".format(n=len(score_table), s=semester))
    )
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=subject[1][:len(subject[1]) - 6],  # (экз.) or (зач.) are 6 last charachters of a subject title
            callback_data="s_t {n} {s}".format(n=int(subject[0]) - 1, s=semester)  # begin counting with 0, not with 1
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
        InlineKeyboardButton(text=b_, callback_data="b_s {b_}".format(b_=b_)) for b_ in BUILDINGS
    ])

    return buildings_dailer_keyboard

def libraries_dailer():
    libraries_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dailer_keyboard.add(*[
        InlineKeyboardButton(text=l_, callback_data="l_s {l_}".format(l_=l_)) for l_ in LIBRARIES
    ])

    return libraries_dailer_keyboard

def dorms_dailer():
    dorms_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dailer_keyboard.add(*[
        InlineKeyboardButton(text=d_, callback_data="d_s {d_}".format(d_=d_)) for d_ in DORMS
    ])

    return dorms_dailer_keyboard

# Remove keyboard
def remove_keyboard():
    return ReplyKeyboardRemove()
