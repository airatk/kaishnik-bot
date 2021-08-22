from enum import Enum


class Option(Enum):
    EMPTY = ""
    
    # /broadcast
    USERS = "users"
    MESSAGE = "message"
    SIGNED = "signed"
    
    # /daysoff
    ADD = "add"
    DROP = "drop"

    # /donated
    AMOUNT = "amount"
    DONATOR = "donator"
    DATE = "date"

class Value(Enum):
    ME = "me"
    
    ALL = "all"
    
    SETUP = "setup"
    UNSETUP = "unsetup"
    
    GROUPS = "groups"
    COMPACTS = "compacts"
    BBS = "bbs"
    UNDEFINED = "undefined"
    
    GUARDS = "guards"
    
    LIST = "list"
