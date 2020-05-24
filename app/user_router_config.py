from fastapi_users import FastAPIUsers

from app.config import SECRET_KEY
from app.database_config import UsersPydantic
from app.user_authentication import auth_backends
from app.user_models import User, UserCreate, UserDB, UserUpdate

fastapi_users = FastAPIUsers(
    UsersPydantic,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
    SECRET_KEY,
)
