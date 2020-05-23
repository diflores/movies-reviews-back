from fastapi_users import models


class User(models.BaseUser):
    first_name: str
    last_name: str


class UserCreate(User, models.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(User, models.BaseUserUpdate):
    first_name: str
    last_name: str


class UserDB(User, models.BaseUserDB):
    first_name: str
    last_name: str
