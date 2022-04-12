from typing import List

from app.models.domain.nfts import NFT
from app.models.domain.ramenmodel import RamenModel

# from typing import Optional


class Profile(RamenModel):
    user_id: int
    wallet_address: str
    nfts: List[NFT]
    # bio: str = ""
    # image: Optional[str] = None
    # following: bool = False
