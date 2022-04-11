from datetime import datetime
from datetime import timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from app.models.domain.users import User
from app.models.schemas.jwt import JWTMeta
from app.models.schemas.jwt import JWTUser

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 * 24  # 24 weeks


def create_jwt_token(
    *, jwt_content: Dict[str, str], secret_key: str, expires_delta: timedelta
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(user: User, secret_key: str) -> str:
    return create_jwt_token(
        jwt_content=JWTUser(id=user.id_, wallet_address=user.wallet_address).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def get_user_id_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).id
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
