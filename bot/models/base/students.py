from peewee import AutoField
from peewee import ForeignKeyField

from bot.models.base.base import Base

from bot.models.users import Users


class Students(Base):
    user_id: ForeignKeyField = ForeignKeyField(model=Users, unique=True, index=True, on_delete="CASCADE")
    
    student_id: AutoField = AutoField()
