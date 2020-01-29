from enum import Enum


class Suboption(Enum):
    ALL: str = "all"
    UNLOGIN: str = "unlogin"
    ME: str = "me"

class DataOption(Enum):
    IDS: str = "ids"
    USERNAME: str = "username"
    FIRSTNAME: str = "firstname"
    NUMBER: str = "number"
    INDEX: str = "index"
    NAME: str = "name"
    GROUP: str = "group"
    YEAR: str = "year"
