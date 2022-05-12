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
headers["X-API-KEY"] = SETTINGS.opensea_api_key


async def get_nft_list(
    nfts_repo: NFTsRepository,
    wallet_address: str,
    user_id: int,
    limit: int = 20,
    cursor: Optional[str] = None,
) -> OpenseaNFTListResponse:
    whitelist = SETTINGS.whitelist_contract_address

    if cursor is None:
        url = (
            f"https://api.opensea.io/api/v1/assets?owner={wallet_address}&limit={limit}"
        )
    else:
        url = f"https://api.opensea.io/api/v1/assets?owner={wallet_address}&limit={limit}&cursor={cursor}"
    
    url_k = f"{url}&collection=kojiroutaipei"
    
    for wl in whitelist:
        url = f"{url}&asset_contract_addresses={wl}"

    # Smart Contract
    resp = requests.get(url, headers=headers)
    list = []
    if resp.status_code == 200:
        jsons = json.loads(resp.text)
        next_cursor = jsons["next"]
        previous_cursor = jsons["previous"]
        for asset in jsons["assets"]:
            token_id = int(asset["token_id"])
            token_address = asset["asset_contract"]["address"]
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

        # Trouble kojiroutaipei
        resp_k = requests.get(url_k, headers=headers)
        if resp_k.status_code == 200:
            jsons_k = json.loads(resp_k.text)
            for asset_k in jsons_k["assets"]:
                token_id = asset_k["name"].split("#")[1]
                token_id = int(token_id.split(' ')[0])
                token_address = "kojiroutaipei"
                name = asset_k["name"]
                image_url = asset_k["image_url"]
                symbol = asset_k["asset_contract"]["symbol"]

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
        print(f"request url: {url}")
        raise Exception("something wrong with opensea api")
