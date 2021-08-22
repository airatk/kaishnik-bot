from peewee import AutoField
from peewee import ForeignKeyField
from peewee import BooleanField

from bot.models.base import Base
from bot.models.user import User


class Settings(Base):
    settings_id: AutoField = AutoField()

    user: ForeignKeyField = ForeignKeyField(model=User, unique=True, index=True, on_delete="CASCADE")
    
    is_schedule_size_full: BooleanField = BooleanField(default=True)
