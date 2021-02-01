from enum import Enum


class Option(Enum):
    EMPTY: str = ""
    
    # /metrics
    DATE: str = "date"
    MONTH: str = "month"
    
    # /data
    NUMBER: str = "number"
    STATE: str = "state"
    USER_ID: str = "user-id"
    
    USERNAME: str = "username"
    FIRSTNAME: str = "firstname"
    
    NAME: str = "name"
    GROUP: str = "group"
    
    BB_LOGIN: str = "bb-login"
    
    # /broadcast
    USERS: str = "users"
    MESSAGE: str = "message"
    SIGNED: str = "signed"
    
    # /daysoff
    ADD: str = "add"
    DROP: str = "drop"

class Value(Enum):
    ME: str = "me"
    
    ALL: str = "all"
    
    SETUP: str = "setup"
    UNSETUP: str = "unsetup"
    
    GROUPS: str = "groups"
    COMPACTS: str = "compacts"
    EXTENDEDS: str = "extendeds"
    BBS: str = "bbs"
    UNDEFINED: str = "undefined"
    
    GUARDS: str = "guards"
    
    LIST: str = "list"
