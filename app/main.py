from typing import List

import requests
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.config import DATABASE_URI, MOVIE_DATABASE_API_KEY, MOVIE_DATABASE_BASE_URL, PRODUCTION_URL
from app.database_config import Reviews, ReviewsPydantic
from app.review_models import ReviewSchema
from app.user_models import User
from app.user_router_config import fastapi_users

app = FastAPI()

origins = [
    "http://localhost:8080",
]
if PRODUCTION_URL:
    origins.append(PRODUCTION_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_dependency = Depends(fastapi_users.get_current_active_user)

app.include_router(fastapi_users.router, prefix="/users", tags=["users"])
register_tortoise(
    app,
    db_url=DATABASE_URI,
    modules={"models": ["app.database_config"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/")
def home():
    return {"Hello": "World"}


# Protected route: Only available if user is logged in.
@app.get("/search-movie")
def search_movie(movie_title: str, user: User = user_dependency):
    response = requests.get(f"{MOVIE_DATABASE_BASE_URL}", params={
                            "api_key": MOVIE_DATABASE_API_KEY, "query": movie_title})
    return response.json()


# Protected route: Only available if user is logged in.
@app.post("/reviews", response_model=ReviewsPydantic)
async def post_new_review(review: ReviewSchema, user: User = user_dependency):
    review_dict = review.dict(exclude_unset=True)
    review_dict["user_id"] = user.id
    new_review = await Reviews.create(**review_dict)
    return await ReviewsPydantic.from_tortoise_orm(new_review)


# Protected route: Only available if user is logged in.
@app.get("/reviews", response_model=List[ReviewsPydantic])
async def get_all_reviews(user: User = user_dependency):
    return await ReviewsPydantic.from_queryset(Reviews.all())


# Protected route: Only available if user is logged in.
@app.get("/users/{user_id}/reviews")
async def get_user_reviews(user_id: str, user: User = user_dependency):
    print(Reviews.get(user=user_id))
    return await ReviewsPydantic.from_queryset(Reviews.filter(user=user_id))
