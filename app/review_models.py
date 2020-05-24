from pydantic import BaseModel


class ReviewSchema(BaseModel):
    movie_id: int
    review: str
