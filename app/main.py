from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.config import DATABASE_URI
from app.user_router_config import fastapi_users

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fastapi_users.router, prefix="/users", tags=["users"])
register_tortoise(
    app,
    db_url=DATABASE_URI,
    modules={"models": ["app.database_config"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


# @fastapi_users.on_after_register()
# def on_after_register(user: User, request: Request):
#     print(f"User {user.id} has registered.")


# @fastapi_users.on_after_forgot_password()
# def on_after_forgot_password(user: User, token: str, request: Request):
#     print(f"User {user.id} has forgot their password. Reset token: {token}")

@app.get('/protected-route', dependencies=[Depends(fastapi_users.get_current_user)])
def protected_route():
    return 'Hello, some user.'
