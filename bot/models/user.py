from datetime import datetime

from peewee import AutoField
from peewee import DateTimeField
from peewee import BigIntegerField
from peewee import TextField
from peewee import BooleanField

from bot.models.base import Base


class User(Base):
    user_id: AutoField = AutoField()
    
    start_datetime: DateTimeField = DateTimeField(default=datetime.now)
    telegram_id: BigIntegerField = BigIntegerField(unique=True, null=True, index=True)
    vk_id: BigIntegerField = BigIntegerField(unique=True, null=True, index=True)

    bb_login: TextField = TextField(null=True)
    bb_password: TextField = TextField(null=True)

    group: TextField = TextField(null=True)
    group_schedule_id: TextField = TextField(null=True)
    
    is_setup: BooleanField = BooleanField(default=False)
    is_group_chat: BooleanField = BooleanField(default=False)
