from fastapi_users import FastAPIUsers

from app.config import SECRET_KEY
from app.user_authentication import auth_backends
from app.models import User, UserCreate, UserUpdate, UserDB
from app.database_config import user_db

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
    SECRET_KEY,
)
