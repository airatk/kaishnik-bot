from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students

from bot.commands.edit.utilities.keyboards import weektype_chooser
from bot.commands.edit.utilities.keyboards import weekday_chooser
from bot.commands.edit.utilities.keyboards import edit_chooser

from bot.shared.helpers import top_notification
from bot.shared.api.subject import StudentSubject
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekParity
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        callback.data in [ Commands.EDIT_SHOW.value, Commands.EDIT_DELETE.value ]
)
@top_notification
async def choose_weetype(callback: CallbackQuery):
    if callback.data == Commands.EDIT_SHOW.value: ACTION: Commands = Commands.EDIT_SHOW_WEEKTYPE
    elif callback.data == Commands.EDIT_DELETE.value: ACTION: Commands = Commands.EDIT_DELETE_WEEKTYPE
    
    (classes_on_both, classes_on_even, classes_on_odd) = (0, 0, 0)
    
    for edited_subject in students[callback.message.chat.id].edited_subjects:
        if edited_subject.is_even is None: classes_on_both += 1
        elif edited_subject.is_even is True: classes_on_even += 1
        elif edited_subject.is_even is False: classes_on_odd += 1
    
    await callback.message.edit_text(
        text=(
            "В скобках указано количество отредактированных пар.\n\n"
            "Выбери тип недели:"
        ),
        reply_markup=weektype_chooser(
            classes_on_both=classes_on_both,
            classes_on_even=classes_on_even,
            classes_on_odd=classes_on_odd,
            ACTION=ACTION
        )
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and (
            Commands.EDIT_SHOW_WEEKTYPE.value in callback.data or
            Commands.EDIT_DELETE_WEEKTYPE.value in callback.data
        )
)
@top_notification
async def choose_weekday(callback: CallbackQuery):
    if Commands.EDIT_SHOW_WEEKTYPE.value in callback.data: ACTION: Commands = Commands.EDIT_SHOW_WEEKDAY
    elif Commands.EDIT_DELETE_WEEKTYPE.value in callback.data: ACTION: Commands = Commands.EDIT_DELETE_WEEKDAY
    
    weektype: str = callback.data.split()[1]
    
    if weektype == WeekParity.BOTH.value: is_even: bool = None
    elif weektype == WeekParity.EVEN.value: is_even: bool = True
    elif weektype == WeekParity.ODD.value: is_even: bool = False
    
    await callback.message.edit_text(
        text="Выбери день:",
        reply_markup=weekday_chooser(
            weektype=callback.data.split()[1],
            subjects_number_by_weekdays=[ sum(1 for subject in students[callback.message.chat.id].edited_subjects if subject.is_even == is_even and subject.weekday == weekday) for weekday in WEEKDAYS ],
            ACTION=ACTION
        )
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and (
            Commands.EDIT_SHOW_WEEKDAY.value in callback.data or
            Commands.EDIT_DELETE_WEEKDAY.value in callback.data
        )
)
@top_notification
async def choose_edit(callback: CallbackQuery):
    if Commands.EDIT_SHOW_WEEKDAY.value in callback.data: ACTION: Commands = Commands.EDIT_SHOW_EDIT
    elif Commands.EDIT_DELETE_WEEKDAY.value in callback.data: ACTION: Commands = Commands.EDIT_DELETE_EDIT
    
    (weektype, weekday) = callback.data.split()[1:]
    
    if weektype == WeekParity.BOTH.value: is_even: bool = None
    elif weektype == WeekParity.EVEN.value: is_even: bool = True
    elif weektype == WeekParity.ODD.value: is_even: bool = False
    
    subjects: {int: StudentSubject} = { index: subject for (index, subject) in enumerate(students[callback.message.chat.id].edited_subjects) if subject.is_even == is_even and subject.weekday == int(weekday) }
    
    await callback.message.edit_text(
        text="Выбери пару:",
        reply_markup=edit_chooser(
            weektype=weektype,
            weekday=weekday,
            subjects=subjects,
            ACTION=ACTION
        )
    )


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_SHOW_ALL.value in callback.data
)
@top_notification
async def show_all(callback: CallbackQuery):
    await callback.message.delete()
    
    request_enities: [str] = callback.data.split()[1:]
    
    weektypes: dict = { "каждая": None, "чётная": True, "нечётная": False }
    weekdays: dict = WEEKDAYS
    
    if len(request_enities) > 0:
        if request_enities[0] == WeekParity.BOTH.value: weektypes = { "каждая": None }
        elif request_enities[0] == WeekParity.EVEN.value: weektypes = { "чётная": True }
        elif request_enities[0] == WeekParity.ODD.value: weektypes = { "нечётная": False }
    
    if len(request_enities) > 1:
        requested_weekday: int = int(request_enities[1])
        weekdays = { requested_weekday: WEEKDAYS[requested_weekday] }
    
    subjects_number: int = 0
    
    for (weektype, is_even) in weektypes.items():
        weektype_weekdays: [str] = [ "*{} неделя*".format(weektype) ]
        
        for (weekday, weekday_name) in weekdays.items():
            weekday_classes: [str] = [ subject.get() for subject in students[callback.message.chat.id].edited_subjects if subject.weekday == weekday and subject.is_even == is_even ]
            
            if len(weekday_classes) > 0:
                subjects_number += len(weekday_classes)
                weektype_weekdays.append("".join([ "*", weekday_name, "*", ] + weekday_classes))
        
        if len(weektype_weekdays) > 1:
            for weektype_weekday in weektype_weekdays:
                await callback.message.answer(
                    text=weektype_weekday,
                    parse_mode="markdown"
                )
    
    if subjects_number == 1: grammatical_entity: str = "а"
    elif subjects_number in range(2, 5): grammatical_entity: str = "ы"
    else: grammatical_entity: str = ""
    
    await callback.message.answer(
        text="*{}* пар{} всего!".format(subjects_number, grammatical_entity),
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_SHOW_EDIT.value in callback.data
)
@top_notification
async def show_edit(callback: CallbackQuery):
    index: int = int(callback.data.split()[1])
    subject: StudentSubject = students[callback.message.chat.id].edited_subjects[index]
    
    await callback.message.edit_text(
        text=subject.get(),
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.drop()


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_DELETE_ALL.value in callback.data
)
@top_notification
async def delete_all(callback: CallbackQuery):
    request_enities: [str] = callback.data.split()[1:]
    
    weektypes: {str: bool} = { "каждая": None, "чётная": True, "нечётная": False }
    weekdays: {int: str} = WEEKDAYS
    
    if len(request_enities) > 0:
        if request_enities[0] == WeekParity.BOTH.value: weektypes = { "каждая": None }
        elif request_enities[0] == WeekParity.EVEN.value: weektypes = { "чётная": True }
        elif request_enities[0] == WeekParity.ODD.value: weektypes = { "нечётная": False }
    
    if len(request_enities) > 1:
        requested_weekday: int = int(request_enities[1])
        weekdays: {int: str} = { requested_weekday: WEEKDAYS[requested_weekday] }
    
    for is_even in weektypes.values():
        for weekday in weekdays:
            for subject in list(students[callback.message.chat.id].edited_subjects):
                if subject.weekday == weekday and subject.is_even == is_even:
                    students[callback.message.chat.id].edited_subjects.remove(subject)
    
    await callback.message.edit_text(text="Удалено!")
    
    students[callback.message.chat.id].guard.drop()
    
    save_data(file=USERS_FILE, object=students)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_DELETE_EDIT.value in callback.data
)
@top_notification
async def delete_edit(callback: CallbackQuery):
    index: int = int(callback.data.split()[1])
    students[callback.message.chat.id].edited_subjects.pop(index)
    
    await callback.message.edit_text(text="Удалено!")
    
    students[callback.message.chat.id].guard.drop()
    
    save_data(file=USERS_FILE, object=students)
