from typing import Optional

from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.ramenmodel import RamenModel


class Comment(IDModelMixin, DateTimeModelMixin, RamenModel):
    post_id: int
    user_id: Optional[int] = None
    user_image: Optional[str] = None
    body: Optional[str] = None
    status: int


class CommentWithWalletAddress(Comment):
    user_wallet_address: Optional[str] = None
