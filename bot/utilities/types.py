from enum import Enum

from typing import List
from typing import Dict
from typing import Tuple
from typing import Optional
from typing import Any


class Platform(Enum):
    TELEGRAM = "telegram"
    VK = "vk"

class Command(Enum):
    CREATOR = "creator"
    USERS = "users"
    METRICS = "metrics"
    CLEAR = "clear"
    ERASE = "erase_"
    DROP = "drop"
    BROADCAST = "broadcast"
    DAYSOFF = "daysoff"
    DONATED = "donated"
    
    NO_PERMISSIONS = "no-permissions"
    
    CANCEL = "cancel"
    
    START = "start"
    RESTART = "start"
    
    LOGIN = "login"
    LOGIN_PLATFORM = "login-platform"
    LOGIN_BB = "login-bb"
    LOGIN_COMPACT = "login-сompact"
    LOGIN_WRONG_GROUP_GUESS = "login-wrong-group-guess"
    LOGIN_CORRECT_GROUP_GUESS = "login-correct-group-guess"
    LOGIN_SET_BB_LOGIN = "login-set-bb-login"
    LOGIN_SET_BB_PASSWORD = "login-set-bb-password"
    LOGIN_SET_GROUP = "login-set-group-"
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
    SCORE_SUBJECT = "score-subject"
    SCORE_MORE_SUBJECTS = "score-more-subjects"
    
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


class Guard:
    def __init__(self):
        self.text: Optional[str] = None
        self.message: Optional[Any] = None
    
    def drop(self):
        self.__init__()

class State:
    def __init__(self):
        # /classes & /exams
        self.another_group_schedule_id: Optional[str] = None
        self.chosen_schedule_dates: List[str] = []
        
        # /lecturers
        self.lecturers_names: List[Dict[str, str]] = []
        
        # /score
        self.auth_token: Optional[str] = None
        self.token_JSESSIONID: Optional[str] = None
        self.semesters: List[str] = []
        self.choosen_semester: Optional[str] = None
        self.score: List[Tuple[str, str]] = []
    
    def drop(self):
        self.__init__()


class SettingsOption(Enum):
    IS_SCHEDULE_SIZE_FULL = "is_schedule_size_full"
