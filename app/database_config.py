import requests
from fastapi_users.db import TortoiseBaseUserModel, TortoiseUserDatabase
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from app.config import MOVIE_DATABASE_API_KEY, MOVIE_DATABASE_BASE_URL
from app.user_models import UserDB


class Users(TortoiseBaseUserModel):
    first_name = fields.CharField(index=True, unique=False, null=False, max_length=255)
    last_name = fields.CharField(index=True, unique=False, null=False, max_length=255)


class Reviews(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="reviews")
    movie_id = fields.IntField(unique=False)
    review = fields.TextField(unique=False)
    rating = fields.IntField(unique=False, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def movie_name(self) -> str:
        response = requests.get(f"{MOVIE_DATABASE_BASE_URL}/movie/{self.movie_id}", params={
            "api_key": MOVIE_DATABASE_API_KEY
        }).json()
        return response["title"]

    class PydanticMeta:
        computed = ["movie_name"]
        exclude = ["user.hashed_password", "user.reviews", "user.is_active", "user.is_superuser"]
        allow_cycles = True
        max_recursion = 4


Tortoise.init_models(["__main__"], "models")
Tortoise.init_models(["app.database_config"], "models")
UsersPydantic = TortoiseUserDatabase(UserDB, Users)
ReviewsPydantic = pydantic_model_creator(Reviews)
