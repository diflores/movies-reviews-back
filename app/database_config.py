from fastapi_users.db import TortoiseBaseUserModel, TortoiseUserDatabase
from tortoise import fields

from app.models import UserDB


class Users(TortoiseBaseUserModel):
    first_name = fields.CharField(index=True, unique=False, null=False, max_length=255)
    last_name = fields.CharField(index=True, unique=False, null=False, max_length=255)


user_db = TortoiseUserDatabase(UserDB, Users)
