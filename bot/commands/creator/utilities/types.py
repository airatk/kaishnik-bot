from enum import Enum


class DataOption(Enum):
    ALL: str = "all"
    UNLOGIN: str = "unlogin"
    ME: str = "me"
    USERNAME: str = "username"
    FIRSTNAME: str = "firstname"
    NUMBER: str = "number"
    INDEX: str = "index"
    FULLNAME: str = "fullname"
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
