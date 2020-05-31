import datetime
from typing import Optional

from pydantic import BaseModel


class ReviewSchemaBasic(BaseModel):
    movie_id: int
    review: str
    rating: Optional[int]


class ReviewSchemaShow(ReviewSchemaBasic):
    user_id: str
    created_at: datetime.datetime
    user_first_name: str
    user_last_name: str
    user_email: str
