from enum import Enum

from typing import List
from typing import Dict
from typing import Tuple
from typing import Optional
from typing import Any


class Guard:
    def __init__(self):
        self.text: Optional[str] = None
        self.message: Optional[Any] = None
    
    def drop(self):
        self.__init__()

class State:
    def __init__(self):
        # /login
        self.groups: List[Tuple[str, str]] = []
        self.group_names: Dict[str, str] = {}
        
        # /classes & /exams
        self.another_group_schedule_id: str = None
        self.chosen_schedule_dates: List[str] = []
        self.classes_offline: Dict[str, List[Dict[str, str]]] = []
        
        # /lecturers
        self.lecturers_names: List[Dict[str, str]] = None
        
        # /score
        self.scoretable: List[Tuple[str, str]] = None
    
    def drop(self):
        self.group_names = {}
        self.another_group_schedule_id = None
        self.chosen_schedule_dates = []
        self.lecturers_names = None
        self.scoretable = None
    
    def drop_all(self):
        self.__init__()


class Commands(Enum):
    CREATOR = "creator"
    USERS = "users"
    METRICS = "metrics"
    CLEAR = "clear"
    ERASE = "erase_"
    DROP = "drop"
    BROADCAST = "broadcast"
    DAYSOFF = "daysoff"
    
    NO_PERMISSIONS = "no-permissions"
    
    CANCEL = "cancel"
    
    START = "start"
    RESTART = "start"
    
    LOGIN = "login"
    LOGIN_PLATFORM = "login-platform"
    LOGIN_COMPACT = "login-сompact"
    LOGIN_EXTENDED = "login-extended"
    LOGIN_WRONG_GROUP_GUESS = "login-wrong-group-guess"
    LOGIN_CORRECT_GROUP_GUESS = "login-correct-group-guess"
    LOGIN_SET_INSTITUTE = "login-set-institute-"
    LOGIN_SET_YEAR = "login-set-year-"
    LOGIN_GROUPS_NEXT_PAGE = "login-groups-next-page-"
    LOGIN_GROUPS_PREVIOUS_PAGE = "login-groups-previous-page-"
    LOGIN_SET_GROUP = "login-set-group-"
    LOGIN_NAMES_NEXT_PAGE = "login-names-next-page-"
    LOGIN_NAMES_PREVIOUS_PAGE = "login-names-previous-page-"
    LOGIN_SET_NAME = "login-set-name-"
    LOGIN_SET_CARD = "login-set-card"
    UNLOGIN = "un-login"

    DELETE_ACCOUNT = "delete-account"
    DELETE_ACCOUNT_CONFIRM = "delete-account-confirm"

    MENU = "menu"
    MORE = "more"

    CLASSES = "classes"
    CLASSES_SHOW = "classes-show"
    CLASSES_CHOOSE = "classes-choose"
    
    EXAMS = "exams"
    
    LECTURERS = "lecturers"
    LECTURERS_NAME = "lecturers-name"
    
    SCORE = "score"
    SCORE_SEMESTER = "score-semester"
    SCORE_ALL = "score-all"
    SCORE_EXAMS = "score-exams"
    SCORE_COURSEWORKS = "score-courseworks"
    SCORE_TESTS = "score-test"
    
    NOTES = "notes"
    NOTES_ADD = "notes-add"
    NOTES_SHOW = "notes-show"
    NOTES_SHOW_ALL = "notes-show-all"
    NOTES_DELETE = "notes-delete"
    NOTES_DELETE_ALL = "notes-delete-all"
    
    EDIT = "edit"
    
    LOCATIONS = "locations"
    
    WEEK = "week"
    BRS = "brs"
    HELP = "help"
    DONATE = "donate"
    DICE = "dice"
    
    SETTINGS = "settings"
    SETTINGS_APPEARANCE = "settings-appearance"
    SETTINGS_APPEARANCE_DONE = "settings-appearance-done"
    SETTINGS_APPEARANCE_DROP = "settings-appearance-drop"
    SETTINGS_PLATFORM_CODE = "settings-platform-code"
    
    UNKNOWN_NONTEXT_MESSAGE = "unknown-nontext-message"
    UNKNOWN_TEXT_MESSAGE = "unknown-text-message"
    UNKNOWN_CALLBACK = "unknown-callback"


class SettingsOption(Enum):
    IS_SCHEDULE_SIZE_FULL = "is_schedule_size_full"
