from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInCreate
from app.models.schemas.users import UserInLogin
from app.models.schemas.users import UserInResponse
from app.models.schemas.users import UserWithToken
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_wallet_address_is_taken

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST, detail=strings.INCORRECT_LOGIN_INPUT
    )

    try:
        user = await users_repo.get_user_by_wallet_address(
            wallet_address=user_login.wallet_address
        )
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    token = jwt.create_access_token_for_user(
        user, str(settings.secret_key.get_secret_value())
    )
    return UserInResponse(
        user=UserWithToken(
            id=user.id_,
            wallet_address=user.wallet_address,
            image=user.image,
            status=user.status,
            token=token,
        )
    )


@router.post(
    "/register",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register",
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    if await check_wallet_address_is_taken(users_repo, user_create.wallet_address):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.WALLET_ADDRESS_TAKEN
        )

    user = await users_repo.create_user(**user_create.dict())
    token = jwt.create_access_token_for_user(
        user, str(settings.secret_key.get_secret_value())
    )
    return UserInResponse(
        user=UserWithToken(
            id=user.id_,
            wallet_address=user.wallet_address,
            image=user.image,
            status=user.status,
            token=token,
        )
    )
