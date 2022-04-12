from typing import List
from typing import Optional

from app.models.domain.nfts import NFT
from app.models.domain.ramenmodel import RamenModel


class Profile(RamenModel):
    user_id: int
    wallet_address: str
    nfts: List[NFT]
    bio: str = ""
    image: Optional[str] = None
    following: bool = False
