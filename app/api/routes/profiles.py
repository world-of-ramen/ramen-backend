from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.dependencies.profiles import get_profile_by_username_from_path
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.nfts import NFTsRepository
from app.db.repositories.profiles import ProfilesRepository
from app.models.domain.profiles import Profile
from app.models.domain.users import User
from app.models.schemas.profiles import ProfileInResponse
from app.resources import strings
from app.services import nft

router = APIRouter()


@router.get("/nfts", response_model=ProfileInResponse, name="profiles:get-nfts")
async def retrieve_nfts(
    user: User = Depends(get_current_user_authorizer()),
    nfts_repo: NFTsRepository = Depends(get_repository(NFTsRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> ProfileInResponse:
    try:
        nfts = await nft.get_all_nft(
            wallet_address=user.wallet_address, user_id=user.id_, nfts_repo=nfts_repo
        )
        profile = Profile(
            user_id=user.id_, wallet_address=user.wallet_address, nfts=nfts
        )
        return ProfileInResponse(profile=profile)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.MALFORMED_PAYLOAD
        )


@router.post(
    "/{username}/follow", response_model=ProfileInResponse, name="profiles:follow-user"
)
async def follow_for_user(
    profile: Profile = Depends(get_profile_by_username_from_path),
    user: User = Depends(get_current_user_authorizer()),
    profiles_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
) -> ProfileInResponse:
    if user.username == profile.username:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.UNABLE_TO_FOLLOW_YOURSELF
        )

    if profile.following:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.USER_IS_ALREADY_FOLLOWED
        )

    await profiles_repo.add_user_into_followers(
        target_user=profile, requested_user=user
    )

    return ProfileInResponse(profile=profile.copy(update={"following": True}))


@router.delete(
    "/{username}/follow",
    response_model=ProfileInResponse,
    name="profiles:unsubscribe-from-user",
)
async def unsubscribe_from_user(
    profile: Profile = Depends(get_profile_by_username_from_path),
    user: User = Depends(get_current_user_authorizer()),
    profiles_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
) -> ProfileInResponse:
    if user.username == profile.username:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.UNABLE_TO_UNSUBSCRIBE_FROM_YOURSELF,
        )

    if not profile.following:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.USER_IS_NOT_FOLLOWED
        )

    await profiles_repo.remove_user_from_followers(
        target_user=profile, requested_user=user
    )

    return ProfileInResponse(profile=profile.copy(update={"following": False}))
