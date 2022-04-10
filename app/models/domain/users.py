from typing import Optional

from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.ramenmodel import RamenModel


class User(IDModelMixin, DateTimeModelMixin, RamenModel):
    wallet_address: str
    image: Optional[str] = None
    status: Optional[int] = None
