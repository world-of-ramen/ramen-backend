from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.users import UserByIdInResponse
from app.models.schemas.users import UserInResponse
from app.models.schemas.users import UserInUpdate
from app.models.schemas.users import UserWithToken
from app.services import jwt


router = APIRouter()


@router.get("", response_model=UserByIdInResponse, name="users:get-current-user")
async def retrieve_current_user(
    user: User = Depends(get_current_user_authorizer()),
    settings: AppSettings = Depends(get_app_settings),
) -> UserByIdInResponse:
    return UserByIdInResponse(user=user)


@router.put("", response_model=UserInResponse, name="users:update-current-user")
async def update_current_user(
    user_update: UserInUpdate = Body(..., embed=True, alias="user"),
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    user = await users_repo.update_user(user=current_user, **user_update.dict())

    token = jwt.create_access_token_for_user(
        user, str(settings.secret_key.get_secret_value())
    )
    return UserInResponse(
        user=UserWithToken(
            id=user.id_,
            wallet_address=user.wallet_address,
            image=user.image,
            token=token,
            status=user.status,
        )
    )
