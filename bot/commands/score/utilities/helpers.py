from bot.shared.api.types import ScoreType
from bot.shared.commands import Commands


def collect_subjects(type: str, scoretable: [(str, str)], attribute_index: int) -> [str]:
    if type == Commands.SCORE_ALL.value:
        return [ subject[attribute_index] for subject in scoretable ]
    if type == Commands.SCORE_EXAMS.value:
        return [ subject[attribute_index] for subject in scoretable if ScoreType.EXAM.value in subject[1] ]
    if type == Commands.SCORE_COURSEWORKS.value:
        return [ subject[attribute_index] for subject in scoretable if ScoreType.COURSEWORK.value in subject[1] ]
    if type == Commands.SCORE_TESTS.value:
        return [ subject[attribute_index] for subject in scoretable if ScoreType.TEST.value in subject[1] ]
    
    return []
