from datetime import datetime

from peewee import AutoField
from peewee import ForeignKeyField
from peewee import DateTimeField
from peewee import TextField

from bot.models.base import Base
from bot.models.user import User


class Note(Base):
    note_id: AutoField = AutoField()

    user: ForeignKeyField = ForeignKeyField(model=User, index=True, on_delete="CASCADE")
    
    creation_datetime: DateTimeField = DateTimeField(default=datetime.now)
    text: TextField = TextField()
