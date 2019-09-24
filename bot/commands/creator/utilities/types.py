from enum import Enum


class DataOption(Enum):
    ALL = "all"
    UNLOGIN = "unlogin"
    ME = "me"
    NUMBER = "number"
    INDEX = "index"
    NAME = "name"
    GROUP = "group"
    YEAR = "year"

class EraseOption(Enum):
    ALL = "all"
    UNLOGIN = "unlogin"
    ME = "me"

class DropOption(Enum):
    ALL = "all"

class ReverseOption(Enum):
    WEEK = "week"
