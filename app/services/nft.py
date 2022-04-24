import json
from typing import Optional

import requests
from loguru import logger
from requests.structures import CaseInsensitiveDict

from app.core.config import get_app_settings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.nfts import NFTsRepository
from app.models.schemas.nfts import NFTListResponse

SETTINGS = get_app_settings()

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-API-Key"] = SETTINGS.moralis_api_key


async def get_nft_list(
    nfts_repo: NFTsRepository,
    wallet_address: str,
    user_id: int,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> NFTListResponse:
    if cursor is None:
        url = f"https://deep-index.moralis.io/api/v2/{wallet_address}/nft?chain=eth&format=decimal&limit={limit}"
    else:
        url = f"https://deep-index.moralis.io/api/v2/{wallet_address}/nft?chain=eth&format=decimal&limit={limit}&cursor={cursor}"

    resp = requests.get(url, headers=headers)
    list = []
    if resp.status_code == 200:
        jsons = json.loads(resp.text)
        cursor = jsons["cursor"]
        total = jsons["total"]
        for r in jsons["result"]:
            token_address = r["token_address"]
            if token_address not in SETTINGS.whitelist_contract_address:
                logger.info(
                    "This address {0} is not in whitelist {1}",
                    token_address,
                    SETTINGS.whitelist_contract_address,
                )
                continue
            token_id = int(r["token_id"])
            name = r["name"]
            symbol = r["symbol"]
            image_url = r["token_uri"]
            try:
                nft = await nfts_repo.get_nft(
                    user_id=user_id,
                    wallet_address=wallet_address,
                    token_address=token_address,
                    token_id=token_id,
                )
                nft = await nfts_repo.update_nft(id=nft.id_, image_url=image_url)
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
        return NFTListResponse(nfts=list, total=total, cursor=cursor)
    else:
        raise Exception("something wrong with moralis api")
