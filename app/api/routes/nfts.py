from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.nfts import NFTsRepository
from app.models.domain.users import User
from app.models.schemas.nfts import OpenseaNFTListResponse
from app.services import opensea_nft


router = APIRouter()


@router.get("/list", response_model=OpenseaNFTListResponse, name="nfts:get-user-nfts")
async def retrieve_nfts(
    limit: int = Query(20, ge=20, le=50),
    cursor: Optional[str] = None,
    user: User = Depends(get_current_user_authorizer()),
    nfts_repo: NFTsRepository = Depends(get_repository(NFTsRepository)),
) -> OpenseaNFTListResponse:
    try:
        return await opensea_nft.get_nft_list(
            nfts_repo=nfts_repo,
            wallet_address=user.wallet_address,
            user_id=user.id_,
            limit=limit,
            cursor=cursor,
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
