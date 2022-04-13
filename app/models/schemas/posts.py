from typing import List
from typing import Optional

from pydantic import BaseModel

from app.models.domain.posts import Post
from app.models.schemas.ramenschema import RamenSchema


class PostInCreate(BaseModel):
    store_id: int
    user_id: Optional[int] = None
    body: Optional[str] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None
    status: int = 1


class PostInUpdate(BaseModel):
    store_id: Optional[int] = None
    user_id: Optional[int] = None
    body: Optional[str] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None
    status: Optional[int] = None


class PostInResponse(RamenSchema):
    post: Post


class PostListResponse(RamenSchema):
    posts: List[Post]
    total: int
