import json

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from siwe.siwe import ExpiredMessage
from siwe.siwe import generate_nonce
from siwe.siwe import InvalidSignature
from siwe.siwe import MalformedSession
from siwe.siwe import SiweMessage
from siwe.siwe import ValidationError
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import Nonce
from app.models.schemas.users import UserInLogin
from app.models.schemas.users import UserInResponse
from app.models.schemas.users import UserWithToken
from app.resources import strings
from app.services import jwt

router = APIRouter()


@router.get("/nonce", status_code=HTTP_200_OK, response_model=Nonce)
async def nonce(settings: AppSettings = Depends(get_app_settings)) -> Nonce:
    return Nonce(nonce=generate_nonce())


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    try:
        siwe_message = SiweMessage(message=json.loads(user_login.message))
        siwe_message.validate(user_login.signature)

        user = await users_repo.get_user_by_wallet_address(
            wallet_address=user_login.wallet_address
        )

        if user is None:
            user = await users_repo.create_user(wallet_address=user_login.wallet_address)

    except (ValidationError, ExpiredMessage, MalformedSession, InvalidSignature):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=strings.INCORRECT_LOGIN_INPUT)

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
