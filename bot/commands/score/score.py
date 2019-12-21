from telebot.types import CallbackQuery
from telebot.types import Message

from bot import bot
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


@bot.message_handler(
    commands=[ Commands.SCORE.value ],
    func=lambda message: students[message.chat.id].guard.text is None
)
@metrics.increment(Commands.SCORE)
def score(message: Message):
    if not students[message.chat.id].is_full:
        bot.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Чтобы видеть номер зачётки и баллы, нужно перенастроиться с зачёткой, отправив /login"
        )
        return
    
    loading_message: Message = bot.send_message(
        chat_id=message.chat.id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    last_available_semester: int = students[message.chat.id].get_last_available_semester()
    
    if last_available_semester is None:
        bot.edit_message_text(
            chat_id=loading_message.chat.id,
            message_id=loading_message.message.id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        return
    
    bot.edit_message_text(
        chat_id=loading_message.chat.id,
        message_id=loading_message.message_id,
        text="Выбери номер семестра:",
        reply_markup=semester_chooser(last_available_semester)
    )
    
    students[message.chat.id].guard.text = Commands.SCORE.value

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SCORE.value and
        Commands.SCORE_SEMESTER.value in callback.data
)
@top_notification
def choose_subjects_type(callback: CallbackQuery):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    semester_number: str = callback.data.split()[1]
    students[callback.message.chat.id].scoretable = students[callback.message.chat.id].get_scoretable(semester_number)
    
    if students[callback.message.chat.id].scoretable is None:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id].guard.drop()
        return
    elif len(students[callback.message.chat.id].scoretable) == 0:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=ResponseError.NO_DATA.value
        )
        
        students[callback.message.chat.id].guard.drop()
        return
    
    (has_exams, has_tests, has_graded_tests) = (False, False, False)
    
    for (_, subject_score) in students[callback.message.chat.id].scoretable:
        if SubjectScoreType.EXAM.value in subject_score: has_exams = True
        elif SubjectScoreType.TEST.value in subject_score: has_tests = True
        elif SubjectScoreType.GRADED_TEST.value in subject_score: has_graded_tests = True
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери тип:",
        reply_markup=subjects_type_chooser(has_exams=has_exams, has_tests=has_tests, has_graded_tests=has_graded_tests)
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SCORE.value and
        callback.data in [ Commands.SCORE_ALL.value, Commands.SCORE_EXAMS.value, Commands.SCORE_TESTS.value, Commands.SCORE_GRADED_TESTS.value ]
)
@top_notification
def choose_subject(callback: CallbackQuery):
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
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери предмет:",
        reply_markup=subject_chooser(subjects=subjects, ACTION=ACTION)
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SCORE.value and (
            Commands.SCORE_ALL.value in callback.data or
            Commands.SCORE_EXAMS.value in callback.data or
            Commands.SCORE_TESTS.value in callback.data or
            Commands.SCORE_GRADED_TESTS.value in callback.data
        )
)
@top_notification
def show_subjects(callback: CallbackQuery):
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
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=subjects[int(string_index)],
            parse_mode="Markdown"
        )
    else:
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
        for subject_score in subjects:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text=subject_score,
                parse_mode="Markdown"
            )
        
        subjects_number: int = len(subjects)
        
        if subjects_number == 1: ending: str = ""
        elif subjects_number in range(2, 5): ending: str = "а"
        else: ending: str = "ов"
        
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="*{subjects_number}* предмет{ending} всего!".format(
                subjects_number=subjects_number, ending=ending
            ),
            parse_mode="Markdown"
        )
    
    students[callback.message.chat.id].guard.drop()
