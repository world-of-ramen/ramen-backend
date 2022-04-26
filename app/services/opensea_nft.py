import json
from typing import Optional

import requests
from requests.structures import CaseInsensitiveDict

from app.core.config import get_app_settings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.nfts import NFTsRepository
from app.models.schemas.nfts import OpenseaNFTListResponse

SETTINGS = get_app_settings()

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-API-Key"] = SETTINGS.moralis_api_key


async def get_nft_list(
    nfts_repo: NFTsRepository,
    wallet_address: str,
    user_id: int,
    limit: int = 20,
    cursor: Optional[str] = None,
) -> OpenseaNFTListResponse:
    whitelist = await nfts_repo.get_whitelist_contract

    if cursor is None:
        url = (
            f"https://api.opensea.io/api/v1/assets?owner={wallet_address}&limit={limit}"
        )
    else:
        url = f"https://api.opensea.io/api/v1/assets?owner={wallet_address}&limit={limit}&cursor={cursor}"

    if len(whitelist) != 0:
        asset_contract_addresses = ",".join(whitelist)
        url = f"{url}&asset_contract_addresses={asset_contract_addresses}"

    resp = requests.get(url, headers=headers)
    list = []
    if resp.status_code == 200:
        jsons = json.loads(resp.text)
        next_cursor = jsons["next"]
        previous_cursor = jsons["previous"]
        for asset in jsons["assets"]:
            token_id = int(asset["token_id"])
            token_address = asset["asset_contract"]["token_address"]
            name = asset["name"]
            image_url = asset["image_url"]
            symbol = asset["asset_contract"]["symbol"]

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
        return OpenseaNFTListResponse(
            nfts=list, previous_cursor=previous_cursor, next_cursor=next_cursor
        )
    else:
        raise Exception("something wrong with moralis api")
