from fastapi_users.db import TortoiseBaseUserModel, TortoiseUserDatabase
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from app.user_models import UserDB


class Users(TortoiseBaseUserModel):
    first_name = fields.CharField(index=True, unique=False, null=False, max_length=255)
    last_name = fields.CharField(index=True, unique=False, null=False, max_length=255)


class Reviews(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="reviews")
    movie_id = fields.IntField(unique=False)
    review = fields.TextField(unique=False)
    created_at = fields.DatetimeField(auto_now_add=True)


Tortoise.init_models(["app.database_config"], "models")
UsersPydantic = TortoiseUserDatabase(UserDB, Users)
ReviewsPydantic = pydantic_model_creator(Reviews, name="Reviews", include=(
                                         "id", "user_id", "movie_id", "review", "created_at"))
