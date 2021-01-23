from bot.models.users import Users
from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.extended_students import ExtendedStudents
from bot.models.bb_students import BBStudents
from bot.models.settings import Settings
from bot.models.notes import Notes
from bot.models.metrics import Metrics
from bot.models.days_off import DaysOff


def setup_database_tables():
    Users.create_table()
    
    GroupsOfStudents.create_table()
    CompactStudents.create_table()
    ExtendedStudents.create_table()
    BBStudents.create_table()
    
    Settings.create_table()
    
    Notes.create_table()
    
    Metrics.create_table()
    DaysOff.create_table()
