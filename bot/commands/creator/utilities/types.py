from enum import Enum


class DataOption(Enum):
    ALL: str = "all"
    UNLOGIN: str = "unlogin"
    ME: str = "me"
    NUMBER: str = "number"
    INDEX: str = "index"
    NAME: str = "name"
    GROUP: str = "group"
    YEAR: str = "year"

class EraseOption(Enum):
    ALL: str = "all"
    UNLOGIN: str = "unlogin"
    ME: str = "me"

class DropOption(Enum):
    ALL: str = "all"

class GuarddropOption(Enum):
    ALL: str = "all"

class ReverseOption(Enum):
    WEEK: str = "week"
