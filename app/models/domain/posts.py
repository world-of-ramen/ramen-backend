from typing import Optional

from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.ramenmodel import RamenModel


class Post(IDModelMixin, DateTimeModelMixin, RamenModel):
    store_id: int
    user_id: Optional[int] = None
    body: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    status: int
