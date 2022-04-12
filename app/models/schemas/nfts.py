from typing import List

from app.models.domain.nfts import NFT
from app.models.schemas.ramenschema import RamenSchema


class NftInResponse(RamenSchema):
    nft: NFT


class NftListResponse(RamenSchema):
    nfts: List[NFT]
