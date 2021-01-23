from typing import List
from typing import Tuple

from bot.utilities.types import Commands
from bot.utilities.api.types import ScoreSubjectType


def collect_subjects(subject_type: str, scoretable: List[Tuple[str, str]], attribute_index: int) -> [str]:
    if subject_type == Commands.SCORE_ALL.value:
        return [ subject[attribute_index] for subject in scoretable ]
    if subject_type == Commands.SCORE_EXAMS.value:
        return [ subject[attribute_index] for subject in scoretable if ScoreSubjectType.EXAM.value in subject[1] ]
    if subject_type == Commands.SCORE_COURSEWORKS.value:
        return [ subject[attribute_index] for subject in scoretable if ScoreSubjectType.COURSEWORK.value in subject[1] ]
    if subject_type == Commands.SCORE_TESTS.value:
        return [ subject[attribute_index] for subject in scoretable if ScoreSubjectType.TEST.value in subject[1] ]
    
    return []
