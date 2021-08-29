from datetime import datetime

from peewee import AutoField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField
from peewee import IntegerField

from bot.models.base import Base
from bot.models.user import User


class Metrics(Base):
    metrics_id: AutoField = AutoField()

    user: ForeignKeyField = ForeignKeyField(model=User, backref="metrics", on_delete="SET NULL", null=True)
    
    platform: TextField = TextField()
    action: TextField = TextField()
    perform_datetime: DateTimeField = DateTimeField(default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"), formats=[ "%Y-%m-%d %H:%M" ])
    usage_number: IntegerField = IntegerField(default=1)
