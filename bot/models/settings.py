from peewee import ForeignKeyField
from peewee import BooleanField

from bot.models.base.base import Base

from bot.models.users import Users


class Settings(Base):
    user_id: ForeignKeyField = ForeignKeyField(model=Users, unique=True, index=True, on_delete="CASCADE")
    
    is_schedule_size_full: BooleanField = BooleanField(default=True)
