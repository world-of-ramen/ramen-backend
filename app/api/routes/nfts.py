from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.nfts import NFTsRepository
from app.models.domain.users import User
from app.models.schemas.nfts import NFTListResponse
from app.resources import strings
from app.services import nft


router = APIRouter()


@router.get("/list", response_model=NFTListResponse, name="nfts:get-user-nfts")
async def retrieve_nfts(
    limit: int = Query(100, ge=1),
    cursor: Optional[str] = None,
    user: User = Depends(get_current_user_authorizer()),
    nfts_repo: NFTsRepository = Depends(get_repository(NFTsRepository)),
) -> NFTListResponse:
    try:
        return await nft.get_nft_list(
            nfts_repo=nfts_repo,
            wallet_address=user.wallet_address,
            user_id=user.id_,
            limit=limit,
            cursor=cursor,
        )
    except Exception:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=strings.NFT_ERROR)


# @router.delete(
#     "/{username}/follow",
#     response_model=ProfileInResponse,
#     name="profiles:unsubscribe-from-user",
# )
# async def unsubscribe_from_user(
#     profile: Profile = Depends(get_profile_by_username_from_path),
#     user: User = Depends(get_current_user_authorizer()),
#     profiles_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
# ) -> ProfileInResponse:
#     if user.username == profile.username:
#         raise HTTPException(
#             status_code=HTTP_400_BAD_REQUEST,
#             detail=strings.UNABLE_TO_UNSUBSCRIBE_FROM_YOURSELF,
#         )

#     if not profile.following:
#         raise HTTPException(
#             status_code=HTTP_400_BAD_REQUEST, detail=strings.USER_IS_NOT_FOLLOWED
#         )

#     await profiles_repo.remove_user_from_followers(
#         target_user=profile, requested_user=user
#     )

#     return ProfileInResponse(profile=profile.copy(update={"following": False}))
