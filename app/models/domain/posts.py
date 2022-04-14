from typing import List
from typing import Optional

from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.comments import CommentWithWalletAddress
from app.models.domain.ramenmodel import RamenModel


class Post(IDModelMixin, DateTimeModelMixin, RamenModel):
    store_id: int
    user_id: Optional[int] = None
    user_wallet_address: Optional[str] = None
    body: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    status: int


class PostWithWalletAddress(Post):
    user_wallet_address: Optional[str] = None


class PostWithComments(PostWithWalletAddress):
    comments: Optional[List[CommentWithWalletAddress]] = None
