from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardRemove

from bot.constants import INSTITUTES
from bot.constants import BUILDINGS
from bot.constants import LIBRARIES
from bot.constants import DORMS


def make_send(command):
    return ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton(text=command))

def skipper(text, callback_data):
    skipper_keyboard = InlineKeyboardMarkup()
    
    skipper_keyboard.row(InlineKeyboardButton(text=text, callback_data=callback_data))

    return skipper_keyboard

def remove_keyboard():
    return ReplyKeyboardRemove()


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
        InlineKeyboardButton(text="сегодня", callback_data="today"),
        InlineKeyboardButton(text="завтра", callback_data="tomorrow")
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="определённую дату", callback_data="certain date"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю", callback_data="weekly crnt"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю", callback_data="weekly next"))

    return schedule_type_keyboard


# /lecturers
def choose_lecturer(names):
    choose_lecturer_keyboard = InlineKeyboardMarkup(row_width=1)

    choose_lecturer_keyboard.add(*[
        InlineKeyboardButton(text=name["lecturer"], callback_data="lecturer {}".format(name["id"])) for name in names
    ])

    return choose_lecturer_keyboard

def lecturer_schedule_type(prepod_login):
    lecturer_schedule_type_keyboard = InlineKeyboardMarkup(row_width=1)

    lecturer_schedule_type_keyboard.add(
        InlineKeyboardButton(text="занятий", callback_data="l-classes {}".format(prepod_login)),
        InlineKeyboardButton(text="экзаменов", callback_data="l-exams {}".format(prepod_login))
    )
    # Cannot write "lecturers classes" because of in-feature usage

    return lecturer_schedule_type_keyboard

def lecturer_classes_week_type(prepod_login):
    week_type_keyboard = InlineKeyboardMarkup(row_width=1)

    week_type_keyboard.add(
        InlineKeyboardButton(text="текущую неделю", callback_data="l-weekly crnt {}".format(prepod_login)),
        InlineKeyboardButton(text="следующую неделю", callback_data="l-weekly next {}".format(prepod_login))
    )

    return week_type_keyboard


# /score
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


# /locations
def choose_location_type():
    location_type_keyboard = InlineKeyboardMarkup()

    location_type_keyboard.row(InlineKeyboardButton(text="Учебные здания и СК", callback_data="buildings_type"))
    location_type_keyboard.row(InlineKeyboardButton(text="Библиотеки", callback_data="libraries_type"))
    location_type_keyboard.row(InlineKeyboardButton(text="Общежития", callback_data="dorms_type"))

    return location_type_keyboard

def buildings_dailer():
    buildings_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dailer_keyboard.add(*[
        InlineKeyboardButton(text=building, callback_data="buildings {}".format(building)) for building in BUILDINGS
    ])

    return buildings_dailer_keyboard

def libraries_dailer():
    libraries_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dailer_keyboard.add(*[
        InlineKeyboardButton(text=library, callback_data="libraries {}".format(library)) for library in LIBRARIES
    ])

    return libraries_dailer_keyboard

def dorms_dailer():
    dorms_dailer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dailer_keyboard.add(*[
        InlineKeyboardButton(text=dorm, callback_data="dorms {}".format(dorm)) for dorm in DORMS
    ])

    return dorms_dailer_keyboard
