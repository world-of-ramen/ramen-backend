from typing import List
from typing import Optional

from pydantic import BaseModel

from app.models.domain.comments import CommentWithWalletAddress
from app.models.schemas.ramenschema import RamenSchema


class CommentInCreate(BaseModel):
    post_id: int
    body: Optional[str] = None
    status: int = 1


class CommentInUpdate(BaseModel):
    body: Optional[str] = None
    status: Optional[int] = None


class CommentInResponse(RamenSchema):
    comment: CommentWithWalletAddress


class CommentListResponse(RamenSchema):
    comments: List[CommentWithWalletAddress]
    total: int
