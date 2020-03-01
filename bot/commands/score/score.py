from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.score.utilities.keyboards import semester_chooser
from bot.commands.score.utilities.keyboards import subjects_type_chooser
from bot.commands.score.utilities.keyboards import subject_chooser

from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import SubjectScoreType
from bot.shared.api.types import ResponseError
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.SCORE.value ]
)
@metrics.increment(Commands.SCORE)
async def score(message: Message):
    if not students[message.chat.id].is_full:
        await message.answer(text="Не доступно :(")
        await message.answer(text="Чтобы видеть номер зачётки и баллы, нужно перенастроиться с зачёткой, отправив /login")
        return
    
    loading_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    last_available_semester: int = students[message.chat.id].get_last_available_semester()
    
    if last_available_semester is None:
        await loading_message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        return
    
    await loading_message.edit_text(
        text="Выбери номер семестра:",
        reply_markup=semester_chooser(last_available_semester)
    )
    
    students[message.chat.id].guard.text = Commands.SCORE.value

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SCORE.value and
        Commands.SCORE_SEMESTER.value in callback.data
)
@top_notification
async def choose_subjects_type(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    semester_number: str = callback.data.split()[1]
    students[callback.message.chat.id].scoretable = students[callback.message.chat.id].get_scoretable(semester_number)
    
    if students[callback.message.chat.id].scoretable is None:
        await callback.message.edit_text(
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id].guard.drop()
        return
    elif len(students[callback.message.chat.id].scoretable) == 0:
        await callback.message.edit_text(text=ResponseError.NO_DATA.value)
        
        students[callback.message.chat.id].guard.drop()
        return
    
    (has_exams, has_tests, has_graded_tests) = (False, False, False)
    
    for (_, subject_score) in students[callback.message.chat.id].scoretable:
        if SubjectScoreType.EXAM.value in subject_score: has_exams = True
        elif SubjectScoreType.TEST.value in subject_score: has_tests = True
        elif SubjectScoreType.GRADED_TEST.value in subject_score: has_graded_tests = True
    
    await callback.message.edit_text(
        text="Выбери тип:",
        reply_markup=subjects_type_chooser(has_exams=has_exams, has_tests=has_tests, has_graded_tests=has_graded_tests)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SCORE.value and
        callback.data in [ Commands.SCORE_ALL.value, Commands.SCORE_EXAMS.value, Commands.SCORE_TESTS.value, Commands.SCORE_GRADED_TESTS.value ]
)
@top_notification
async def choose_subject(callback: CallbackQuery):
    if callback.data == Commands.SCORE_ALL.value:
        subjects: [str] = [ title for (title, _) in students[callback.message.chat.id].scoretable ]
        ACTION: Commands = Commands.SCORE_ALL
    elif callback.data == Commands.SCORE_EXAMS.value:
        subjects: [str] = [ title for (title, subject_score) in students[callback.message.chat.id].scoretable if SubjectScoreType.EXAM.value in subject_score ]
        ACTION: Commands = Commands.SCORE_EXAMS
    elif callback.data == Commands.SCORE_TESTS.value:
        subjects: [str] = [ title for (title, subject_score) in students[callback.message.chat.id].scoretable if SubjectScoreType.TEST.value in subject_score ]
        ACTION: Commands = Commands.SCORE_TESTS
    elif callback.data == Commands.SCORE_GRADED_TESTS.value:
        subjects: [str] = [ title for (title, subject_score) in students[callback.message.chat.id].scoretable if SubjectScoreType.GRADED_TEST.value in subject_score ]
        ACTION: Commands = Commands.SCORE_GRADED_TESTS
    
    await callback.message.edit_text(
        text="Выбери предмет:",
        reply_markup=subject_chooser(subjects=subjects, ACTION=ACTION)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SCORE.value and (
            Commands.SCORE_ALL.value in callback.data or
            Commands.SCORE_EXAMS.value in callback.data or
            Commands.SCORE_TESTS.value in callback.data or
            Commands.SCORE_GRADED_TESTS.value in callback.data
        )
)
@top_notification
async def show_subjects(callback: CallbackQuery):
    (action, string_index) = callback.data.split()
    
    if action == Commands.SCORE_ALL.value:
        subjects: [str] = [ subject_score for (_, subject_score) in students[callback.message.chat.id].scoretable ]
    elif action == Commands.SCORE_EXAMS.value:
        subjects: [str] = [ subject_score for (_, subject_score) in students[callback.message.chat.id].scoretable if SubjectScoreType.EXAM.value in subject_score ]
    elif action == Commands.SCORE_TESTS.value:
        subjects: [str] = [ subject_score for (_, subject_score) in students[callback.message.chat.id].scoretable if SubjectScoreType.TEST.value in subject_score ]
    elif action == Commands.SCORE_GRADED_TESTS.value:
        subjects: [str] = [ subject_score for (_, subject_score) in students[callback.message.chat.id].scoretable if SubjectScoreType.GRADED_TEST.value in subject_score ]
    
    if string_index != "None":
        await callback.message.edit_text(
            text=subjects[int(string_index)],
            parse_mode="markdown"
        )
    else:
        await callback.message.delete()
        
        for subject_score in subjects:
            await callback.message.answer(
                text=subject_score,
                parse_mode="markdown"
            )
        
        subjects_number: int = len(subjects)
        
        if subjects_number == 1: ending: str = ""
        elif subjects_number in range(2, 5): ending: str = "а"
        else: ending: str = "ов"
        
        await callback.message.answer(
            text="*{subjects_number}* предмет{ending} всего!".format(subjects_number=subjects_number, ending=ending),
            parse_mode="markdown"
        )
    
    students[callback.message.chat.id].guard.drop()
