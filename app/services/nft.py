import json
from typing import List

import requests
from fastapi import Depends
from requests.structures import CaseInsensitiveDict

from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.nfts import NFTsRepository
from app.models.domain.nfts import NFT

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers[
    "X-API-Key"
] = "UVOA0GGTEBVMZb3nnepdwnND8RQH2j5tNEGyEHh3xjGYhROQKbS7jWHgp3QvOe7r"


async def get_all_nft(
    wallet_address: str,
    user_id: int,
    nfts_repo: NFTsRepository = Depends(get_repository(NFTsRepository)),
) -> List[NFT]:
    url = f"https://deep-index.moralis.io/api/v2/{wallet_address}/nft?chain=eth&format=decimal"
    resp = requests.get(url, headers=headers)
    list = []
    if resp.status_code == 200:
        jsons = json.loads(resp.text)
        for r in jsons["result"]:
            if r["metadata"] is None:
                continue
            token_address = r["token_address"]
            token_id = r["token_id"]
            name = r["name"]
            symbol = r["symbol"]
            dict = json.loads(r["metadata"])
            image_url = dict["image"]
            try:
                nft = await nfts_repo.get_nft(
                    user_id=user_id,
                    wallet_address=wallet_address,
                    token_address=token_address,
                    token_id=token_id,
                )
                nft = nfts_repo.update_nft(id=nft.id_, image_url=image_url)
                list.append(nft)
            except EntityDoesNotExist:
                nft = await nfts_repo.create_nft(
                    user_id=user_id,
                    wallet_address=wallet_address,
                    image_url=image_url,
                    token_address=token_address,
                    token_id=token_id,
                    name=name,
                    symbol=symbol,
                )
                list.append(nft)
        return list
    else:
        raise Exception("can not access moralis api")
