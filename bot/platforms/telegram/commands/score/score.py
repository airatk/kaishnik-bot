from typing import List

from random import choice

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.score.utilities.keyboards import semester_chooser
from bot.platforms.telegram.commands.score.utilities.keyboards import subject_chooser

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.student import get_score_data


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.SCORE.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.SCORE.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.SCORE)
async def choose_semester(message: Message):
    user: User = User.get(User.telegram_id == message.chat.id)
    
    if user.bb_login is None or user.bb_password is None:
        await message.answer(text="Не доступно :(")
        
        if message.chat.type == ChatType.PRIVATE:
            await message.answer(text="Чтобы видеть баллы, нужно отправить /login и войти через ББ.")
        
        return
    
    loading_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (score_data, response_error) = get_score_data(user=user)
    
    if response_error is not None:
        await loading_message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        return

    states[message.chat.id].auth_token = score_data[0]
    states[message.chat.id].token_JSESSIONID = score_data[1]
    states[message.chat.id].semesters = score_data[2]
    states[message.chat.id].score = score_data[3]
    
    await loading_message.edit_text(
        text="Выбери номер семестра:",
        reply_markup=semester_chooser(semesters=states[message.chat.id].semesters)
    )
    
    guards[message.chat.id].text = Command.SCORE.value

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SCORE.value and
        Command.SCORE_SEMESTER.value in callback.data
)
@top_notification
async def choose_subject(callback: CallbackQuery):
    semester: str = callback.data.split()[1]
    last_semester: str = max(states[callback.message.chat.id].semesters)

    if semester != last_semester:
        await callback.message.edit_text(
            text=choice(LOADING_REPLIES),
            disable_web_page_preview=True
        )

        (score_data, response_error) = get_score_data(
            user=User.get(User.telegram_id == callback.message.chat.id),
            semester=semester,
            auth_token=states[callback.message.chat.id].auth_token,
            token_JSESSIONID=states[callback.message.chat.id].token_JSESSIONID
        )

        if response_error is not None:
            await callback.message.edit_text(
                text=response_error.value,
                disable_web_page_preview=True
            )

            states[callback.message.chat.id].drop()
            guards[callback.message.chat.id].drop()
            return
        
        states[callback.message.chat.id].score = score_data[3]
    
    subjects: List[str] = [ title for (title, _) in states[callback.message.chat.id].score ]

    await callback.message.edit_text(
        text="Выбери предмет:",
        reply_markup=subject_chooser(subjects=subjects)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SCORE.value and 
        Command.SCORE_SUBJECT.value in callback.data
)
@top_notification
async def show_score(callback: CallbackQuery):
    subject_index: str = callback.data.split()[1]
    subjects: List[str] = [ subject for (_, subject) in states[callback.message.chat.id].score ]
    
    if subject_index != "-":
        await callback.message.edit_text(
            text=subjects[int(subject_index)],
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await callback.message.delete()
        
        for subject in subjects:
            await callback.message.answer(
                text=subject,
                parse_mode=ParseMode.MARKDOWN
            )
        
        ending: str = "" if len(subjects) == 1 else "а" if len(subjects) in range(2, 5) else "ов"
        
        await callback.message.answer(
            text=f"*{len(subjects)}* предмет{ending} всего!",
            parse_mode=ParseMode.MARKDOWN
        )
    
    states[callback.message.chat.id].drop()
    guards[callback.message.chat.id].drop()
