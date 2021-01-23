from peewee import ForeignKeyField
from peewee import AutoField
from peewee import TextField

from bot.models.base.base import Base

from bot.models.users import Users


class Notes(Base):
    user_id: ForeignKeyField = ForeignKeyField(model=Users, index=True, on_delete="CASCADE")
    
    note_id: AutoField = AutoField()
    
    note: TextField = TextField(null=True)
