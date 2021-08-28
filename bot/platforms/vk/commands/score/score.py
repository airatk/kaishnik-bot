from typing import List

from random import choice

from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards
from bot.platforms.vk import states

from bot.platforms.vk.commands.score.utilities.keyboards import semester_chooser
from bot.platforms.vk.commands.score.utilities.keyboards import subject_chooser
from bot.platforms.vk.utilities.helpers import is_group_chat
from bot.platforms.vk.utilities.keyboards import to_settings
from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.student import get_score_data


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.payload is None and
        event.object.object.message.text.capitalize() == CommandOfVK.SCORE.value
)
@note_metrics(platform=Platform.VK, command=Command.SCORE)
async def choose_semester(event: SimpleBotEvent):
    user: User = User.get(User.vk_id == event.peer_id)
    
    if user.bb_login is None or user.bb_password is None:
        await event.answer(message="Не доступно :(")
        
        if not is_group_chat(peer_id=event.peer_id):
            await event.answer(
                message="Чтобы видеть баллы, нужно сменить аккаунт в настройках и войти через ББ.",
                keyboard=to_settings()
            )
        
        return
    
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    (score_data, response_error) = get_score_data(user=user)
    
    if response_error is not None:
        await event.answer(
            message=response_error.value,
            dont_parse_links=True
        )
        return

    states[event.peer_id].auth_token = score_data[0]
    states[event.peer_id].token_JSESSIONID = score_data[1]
    states[event.peer_id].semesters = score_data[2]
    states[event.peer_id].score = score_data[3]
    
    await event.answer(
        message="Выбери номер семестра:",
        keyboard=semester_chooser(semesters=states[event.peer_id].semesters)
    )

@vk_bot.message_handler(PayloadContainsFilter(key=Command.SCORE_SEMESTER.value))
async def choose_subject(event: SimpleBotEvent):
    semester: str = event.payload[Command.SCORE_SEMESTER.value]

    if len(states[event.peer_id].semesters) == 0:
        await event.answer(
            message="Что-то пошло не так🙆🏼‍♀️",
            keyboard=to_menu()
        )

        guards[event.peer_id].drop()
        return
    
    last_semester: str = max(states[event.peer_id].semesters)

    if semester != last_semester:
        await event.answer(
            message=choice(LOADING_REPLIES),
            dont_parse_links=True
        )

        (score_data, response_error) = get_score_data(
            user=User.get(User.vk_id == event.peer_id),
            semester=semester,
            auth_token=states[event.peer_id].auth_token,
            token_JSESSIONID=states[event.peer_id].token_JSESSIONID
        )

        if response_error is not None:
            await event.answer(
                message=response_error.value,
                dont_parse_links=True
            )

            states[event.peer_id].drop()
            guards[event.peer_id].drop()
            return
        
        states[event.peer_id].score = score_data[3]
    
    subjects: List[str] = [ title for (title, _) in states[event.peer_id].score ]

    await event.answer(
        message="Выбери предмет:",
        keyboard=subject_chooser(subjects=subjects)
    )

@vk_bot.message_handler(PayloadContainsFilter(key=Command.SCORE_MORE_SUBJECTS.value))
async def show_more_subjects(event: SimpleBotEvent):
    next_offset: int = event.payload[Command.SCORE_MORE_SUBJECTS.value]
    subjects: List[str] = [ title for (title, _) in states[event.peer_id].score ]

    await event.answer(
        message="Ещё предметы:",
        keyboard=subject_chooser(subjects=subjects, offset=next_offset)
    )

@vk_bot.message_handler(PayloadContainsFilter(key=Command.SCORE_SUBJECT.value))
async def show_score(event: SimpleBotEvent):
    subject_index: int = event.payload[Command.SCORE_SUBJECT.value]
    subjects: List[str] = [ subject for (_, subject) in states[event.peer_id].score ]

    if subject_index >= len(subjects) or len(subjects) == 0:
        await event.answer(
            message="Что-то пошло не так🙆🏼‍♀️",
            keyboard=to_menu()
        )

        guards[event.peer_id].drop()
        return

    if subject_index == -1:
        for subject in subjects:
            await event.answer(
                message=remove_markdown(subject),
                keyboard=to_menu()
            )
        
        ending: str = "" if len(subjects) == 1 else "а" if len(subjects) in range(2, 5) else "ов"

        await event.answer(message=f"{len(subjects)} предмет{ending} всего!")
    else:
        await event.answer(
            message=remove_markdown(subjects[subject_index]),
            keyboard=to_menu()
        )
