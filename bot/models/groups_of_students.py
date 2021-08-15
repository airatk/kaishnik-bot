from peewee import ForeignKeyField
from peewee import AutoField
from peewee import TextField

from bot.models.base.base import Base
from bot.models.users import Users


class GroupsOfStudents(Base):
    user_id: ForeignKeyField = ForeignKeyField(model=Users, unique=True, index=True, on_delete="CASCADE")
    
    group_id: AutoField = AutoField()
    
    group: TextField = TextField(null=True)
    group_schedule_id: TextField = TextField(null=True)
