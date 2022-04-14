from typing import List
from typing import Optional

from pydantic import BaseModel

from app.models.domain.posts import PostWithComments
from app.models.domain.posts import PostWithWalletAddress
from app.models.schemas.ramenschema import RamenSchema


class PostInCreate(BaseModel):
    store_id: int
    body: Optional[str] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None
    status: int = 1


class PostInUpdate(BaseModel):
    body: Optional[str] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None
    status: Optional[int] = None


class PostInResponse(RamenSchema):
    post: PostWithWalletAddress


class PostListResponse(RamenSchema):
    posts: List[PostWithComments]
    total: int
