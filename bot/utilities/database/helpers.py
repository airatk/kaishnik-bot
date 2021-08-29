from bot.models.user import User
from bot.models.settings import Settings
from bot.models.note import Note
from bot.models.metrics import Metrics
from bot.models.day_off import DayOff
from bot.models.donation import Donation


def setup_database_tables():
    User.create_table()
    Settings.create_table()
    Note.create_table()
    
    Metrics.create_table()
    DayOff.create_table()
    Donation.create_table()
