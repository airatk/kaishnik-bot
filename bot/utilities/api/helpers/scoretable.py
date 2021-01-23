from typing import List
from typing import Tuple

from bot.utilities.api.types import ScoreSubjectType


def beautify_scoretable(raw_scoretable: List[List[str]]) -> List[Tuple[str, str]]:
    scoretable: List[Tuple[str, str]] = []
    
    for subject in raw_scoretable:
        unstyled_title: str = subject[1].replace("(экз.)", "").replace("(зач.)", "").replace("(зач./оц.)", "")
        title: str = "*{title}*".format(title=unstyled_title)
        
        if "(экз.)" in subject[1]:
            subject_type: str = "".join([ "\n_", ScoreSubjectType.EXAM.value, "_\n" ])
        elif "(зач./оц.)" in subject[1]:
            subject_type: str = "".join([ "\n_", ScoreSubjectType.COURSEWORK.value, "_\n" ])
        elif "(зач.)" in subject[1]:
            subject_type: str = "".join([ "\n_", ScoreSubjectType.TEST.value, "_\n" ])
        else:
            subject_type: str = "".join([ "\n_", ScoreSubjectType.OTHER.value, "_\n" ])
        
        certification1: str = "\n• 1 аттестация: {gained} / {max}".format(gained=subject[2], max=subject[3])
        certification2: str = "\n• 2 аттестация: {gained} / {max}".format(gained=subject[4], max=subject[5])
        certification3: str = "\n• 3 аттестация: {gained} / {max}".format(gained=subject[6], max=subject[7])
        
        score_sum: str = "\n\n• За семестр: {gained} / {max}".format(
            gained=subject[8],
            max=sum(map(lambda certification_max:
                int(certification_max) if certification_max.isnumeric() else 0,
                [ subject[3], subject[5], subject[7] ]
            ))
        )
        debts: str = "\n• Долги: {}".format(subject[10])
        
        scoretable.append((
            unstyled_title,
            "".join([ title, subject_type, certification1, certification2, certification3, score_sum, debts ])
        ))
    
    return scoretable
