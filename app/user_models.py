from fastapi_users import models


class User(models.BaseUser):
    first_name: str
    last_name: str


class UserCreate(User, models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass
