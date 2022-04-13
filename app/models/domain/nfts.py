from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.ramenmodel import RamenModel


class NFT(IDModelMixin, DateTimeModelMixin, RamenModel):
    user_id: int
    wallet_address: str
    image_url: str
    token_address: str
    token_id: str
    name: str
    symbol: str
