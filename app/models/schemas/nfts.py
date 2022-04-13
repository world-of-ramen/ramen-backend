from typing import List

from app.models.domain.nfts import NFT
from app.models.schemas.ramenschema import RamenSchema


class NFTInResponse(RamenSchema):
    nft: NFT


class NFTListResponse(RamenSchema):
    nfts: List[NFT]
