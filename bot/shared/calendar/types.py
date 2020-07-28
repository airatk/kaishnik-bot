from enum import Enum


class WeekType(Enum):
    CURRENT: str = "week-current"
    NEXT: str = "week-next"
    PREVIOUS: str = "week-previous"

class WeekParity(Enum):
    BOTH: str = "both"
    EVEN: str = "even"
    ODD: str = "odd"
