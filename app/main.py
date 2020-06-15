# mypy: ignore-errors

from typing import List

import requests
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.config import (
    DATABASE_URI,
    MOVIE_DATABASE_API_KEY,
    MOVIE_DATABASE_BASE_URL,
    SVELTE_PRODUCTION_URL,
    VUE_PRODUCTION_URL,
)
from app.database_config import Reviews, ReviewsPydantic, UsersPydantic
from app.review_models import ReviewSchemaBasic
from app.user_models import User
from app.user_router_config import fastapi_users

app = FastAPI()

origins = [
    "http://localhost:8080",
]

if VUE_PRODUCTION_URL:
    origins.append(VUE_PRODUCTION_URL)

if SVELTE_PRODUCTION_URL:
    origins.append(SVELTE_PRODUCTION_URL)

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
Tortoise.init_models(["__main__"], "models")


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/users/profile/{user_id}", response_model=User)
async def get_user_info(user_id, user: User = user_dependency):
    return await UsersPydantic.get(id=user_id)


# Protected route: Only available if user is logged in.
@app.get("/search-movie")
def search_movie(movie_title: str, user: User = user_dependency):
    response = requests.get(f"{MOVIE_DATABASE_BASE_URL}/search/movie", params={
                            "api_key": MOVIE_DATABASE_API_KEY, "query": movie_title})
    return response.json()


# Protected route: Only available if user is logged in.
@app.get("/discover-movie")
async def get_recommendation(language: str = None,
                             region: str = None,
                             sort_by: str = None,
                             certification_country: str = None,
                             certification: str = None,
                             certification_lte: str = None,
                             certification_gte: str = None,
                             include_adult: bool = None,
                             include_video: bool = None,
                             page: int = None,
                             primary_release_year: int = None,
                             primary_release_date_gte: str = None,
                             primary_release_date_lte: str = None,
                             release_date_gte: str = None,
                             release_date_lte: str = None,
                             with_release_type: int = None,
                             year: int = None,
                             vote_count_gte: int = None,
                             vote_count_lte: int = None,
                             vote_average_gte: float = None,
                             vote_average_lte: float = None,
                             with_cast: str = None,
                             with_crew: str = None,
                             with_people: str = None,
                             with_companies: str = None,
                             with_genres: str = None,
                             without_genres: str = None,
                             with_keywords: str = None,
                             without_keywords: str = None,
                             with_runtime_gte: int = None,
                             with_runtime_lte: int = None,
                             with_original_language: str = None,
                             user: User = user_dependency):
    response = requests.get(f"{MOVIE_DATABASE_BASE_URL}/discover/movie", params={
                            "api_key": MOVIE_DATABASE_API_KEY,
                            "language": language,
                            "region": region,
                            "sort_by": sort_by,
                            "certification_country": certification_country,
                            "certification": certification,
                            "certification.lte": certification_lte,
                            "certification.gte": certification_gte,
                            "include_adult": include_adult,
                            "include_video": include_video,
                            "page": page,
                            "primary_release_year": primary_release_year,
                            "primary_release_date.gte": primary_release_date_gte,
                            "primary_release_date.lte": primary_release_date_lte,
                            "release_date.gte": release_date_gte,
                            "release_date.lte": release_date_lte,
                            "with_release_type": with_release_type,
                            "year": year,
                            "vote_count.gte": vote_count_gte,
                            "vote_count.lte": vote_count_lte,
                            "vote_average.gte": vote_average_gte,
                            "vote_average.lte": vote_average_lte,
                            "with_cast": with_cast,
                            "with_crew": with_crew,
                            "with_people": with_people,
                            "with_companies": with_companies,
                            "with_genres": with_genres,
                            "without_genres": without_genres,
                            "with_keywords": with_keywords,
                            "without_keywords": without_keywords,
                            "with_runtime.gte": with_runtime_gte,
                            "with_runtime.lte": with_runtime_lte,
                            "with_original_language": with_original_language
                            })
    return response.json()


# Protected route: Only available if user is logged in.
@app.get("/movies/{movie_id}")
async def get_movie_info(movie_id=int, user: User = user_dependency):
    response = requests.get(f"{MOVIE_DATABASE_BASE_URL}/movie/{movie_id}", params={
        "api_key": MOVIE_DATABASE_API_KEY
    })
    return response.json()


# Protected route: Only available if user is logged in.
@app.get("/movies/{movie_id}/credits")
async def get_movie_credits(movie_id=int, user: User = user_dependency):
    response = requests.get(f"{MOVIE_DATABASE_BASE_URL}/movie/{movie_id}/credits", params={
        "api_key": MOVIE_DATABASE_API_KEY
    })
    return response.json()


# Protected route: Only available if user is logged in.
@app.post("/reviews", response_model=ReviewsPydantic)
async def post_new_review(review: ReviewSchemaBasic, user: User = user_dependency):
    review_dict = review.dict(exclude_unset=True)
    review_dict["user_id"] = user.id
    new_review = await Reviews.create(**review_dict)
    result = await ReviewsPydantic.from_queryset_single(Reviews.get(id=new_review.id))
    return result


# Protected route: Only available if user is logged in.
@app.get("/movies/{movie_id}/reviews", response_model=List[ReviewsPydantic])
async def get_movie_reviews(movie_id: str, user: User = user_dependency):
    return await ReviewsPydantic.from_queryset(Reviews.filter(movie_id=movie_id))


# Protected route: Only available if user is logged in.
@app.get("/reviews", response_model=List[ReviewsPydantic])
async def get_all_reviews(user: User = user_dependency):
    return await ReviewsPydantic.from_queryset(Reviews.all())


# Protected route: Only available if user is logged in.
@app.get("/users/{user_id}/reviews", response_model=List[ReviewsPydantic])
async def get_user_reviews(user_id: str, user: User = user_dependency):
    return await ReviewsPydantic.from_queryset(Reviews.filter(user=user_id))
