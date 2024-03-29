from typing import List
from typing import Optional

from app.models.domain.nfts import NFT
from app.models.schemas.ramenschema import RamenSchema


class NFTInResponse(RamenSchema):
    nft: NFT


class NFTListResponse(RamenSchema):
    nfts: List[NFT]
    total: int
    cursor: str


class OpenseaNFTListResponse(RamenSchema):
    nfts: List[NFT]
    previous_cursor: Optional[str]
    next_cursor: Optional[str]
