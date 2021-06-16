from enum import Enum

from typing import List
from typing import Dict
from typing import Tuple

from aiogram.types import Message


class Guard:
    def __init__(self):
        self.text: str = None
        self.message: Message = None
    
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
    CREATOR: str = "creator"
    USERS: str = "users"
    METRICS: str = "metrics"
    CLEAR: str = "clear"
    ERASE: str = "erase_"
    DROP: str = "drop"
    BROADCAST: str = "broadcast"
    DAYSOFF: str = "daysoff"
    
    NO_PERMISSIONS: str = "no-permissions"
    
    CANCEL: str = "cancel"
    
    START: str = "start"
    
    LOGIN: str = "login"
    LOGIN_COMPACT: str = "login-сompact"
    LOGIN_EXTENDED: str = "login-extended"
    LOGIN_WRONG_GROUP_GUESS: str = "login-wrong-group-guess"
    LOGIN_CORRECT_GROUP_GUESS: str = "login-correct-group-guess"
    LOGIN_SET_INSTITUTE: str = "login-set-institute-"
    LOGIN_SET_YEAR: str = "login-set-year-"
    LOGIN_GROUPS_NEXT_PAGE: str = "login-groups-next-page-"
    LOGIN_GROUPS_PREVIOUS_PAGE: str = "login-groups-previous-page-"
    LOGIN_SET_GROUP: str = "login-set-group-"
    LOGIN_NAMES_NEXT_PAGE: str = "login-names-next-page-"
    LOGIN_NAMES_PREVIOUS_PAGE: str = "login-names-previous-page-"
    LOGIN_SET_NAME: str = "login-set-name-"
    LOGIN_SET_CARD: str = "login-set-card"
    UNLOGIN: str = "un-login"
    
    CLASSES: str = "classes"
    CLASSES_SHOW: str = "classes-show"
    CLASSES_CHOOSE: str = "classes-choose"
    
    EXAMS: str = "exams"
    
    LECTURERS: str = "lecturers"
    LECTURERS_NAME: str = "lecturers-name"
    
    SCORE: str = "score"
    SCORE_SEMESTER: str = "score-semester"
    SCORE_ALL: str = "score-all"
    SCORE_EXAMS: str = "score-exams"
    SCORE_COURSEWORKS: str = "score-courseworks"
    SCORE_TESTS: str = "score-test"
    
    NOTES: str = "notes"
    NOTES_ADD: str = "notes-add"
    NOTES_SHOW: str = "notes-show"
    NOTES_SHOW_ALL: str = "notes-show-all"
    NOTES_DELETE: str = "notes-delete"
    NOTES_DELETE_ALL: str = "notes-delete-all"
    
    EDIT: str = "edit"
    EDIT_ADD: str = "edit-add"
    EDIT_WEEKTYPE: str = "edit-weektype"
    EDIT_WEEKDAY: str = "edit-weekday"
    EDIT_HOUR: str = "edit-hour"
    EDIT_TIME: str = "edit-time"
    EDIT_BUILDING: str = "edit-building"
    EDIT_AUDITORIUM: str = "edit-auditorium"
    EDIT_SUBJECT_TITLE: str = "edit-subject-title"
    EDIT_SUBJECT_TYPE: str = "edit-subject-title"
    EDIT_LECTURER: str = "edit-lecturer-name"
    EDIT_DEPARTMENT: str = "edit-department"
    EDIT_SHOW: str = "edit-show"
    EDIT_SHOW_ALL: str = "edit-show-all"
    EDIT_SHOW_WEEKTYPE: str = "edit-show-weektype"
    EDIT_SHOW_WEEKDAY: str = "edit-show-weekday"
    EDIT_SHOW_EDIT: str = "edit-show-edit"
    EDIT_DELETE: str = "edit-delete"
    EDIT_DELETE_ALL: str = "edit-delete-all"
    EDIT_DELETE_WEEKTYPE: str = "edit-delete-weektype"
    EDIT_DELETE_WEEKDAY: str = "edit-delete-weekday"
    EDIT_DELETE_EDIT: str = "edit-delete-edit"
    
    LOCATIONS: str = "locations"
    
    WEEK: str = "week"
    BRS: str = "brs"
    HELP: str = "help"
    DONATE: str = "donate"
    DICE: str = "dice"
    
    SETTINGS: str = "settings"
    SETTINGS_APPEARANCE: str = "settings-appearance"
    SETTINGS_APPEARANCE_DONE: str = "settings-appearance-done"
    SETTINGS_APPEARANCE_DROP: str = "settings-appearance-drop"
    
    UNKNOWN_NONTEXT_MESSAGE: str = "unknown-nontext-message"
    UNKNOWN_TEXT_MESSAGE: str = "unknown-text-message"
    UNKNOWN_CALLBACK: str = "unknown-callback"
