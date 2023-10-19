from pydantic import BaseModel, root_validator
from datetime import datetime
from typing import Optional


class BlogSchema(BaseModel):
    id: int
    title: str
    text: str
    date: datetime
    isLiked: bool
    author_name: Optional[str]

    @root_validator(pre=True)
    def formatedField(cls, v):
        # print(v.author)
        v.author_name = v.author.login
        return v
