from enum import Enum


class Option(Enum):
    EMPTY = ""
    
    # /metrics
    DATE = "date"
    MONTH = "month"
    
    # /data
    NUMBER = "number"
    STATE = "state"
    USER_ID = "user-id"
    
    USERNAME = "username"
    FIRSTNAME = "firstname"
    
    NAME = "name"
    GROUP = "group"
    
    BB_LOGIN = "bb-login"
    
    # /broadcast
    USERS = "users"
    MESSAGE = "message"
    SIGNED = "signed"
    
    # /daysoff
    ADD = "add"
    DROP = "drop"

    # /donated
    AMOUNT = "amount"

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
