from pydantic import BaseModel
from datetime import datetime


class PostCreateSchema(BaseModel):
    title: str
    text: str

class PostGetSchema(PostCreateSchema):
    id: int
    date: datetime

    class Config:
        from_attributes = True

class LikeSchema(BaseModel):
    post_id: int
    