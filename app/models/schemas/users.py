from typing import Optional

from pydantic import BaseModel

from app.models.domain.users import User
from app.models.schemas.ramenschema import RamenSchema


class UserInLogin(RamenSchema):
    wallet_address: str


class UserInCreate(BaseModel):
    wallet_address: str
    image: Optional[str] = None


class UserInUpdate(BaseModel):
    image: Optional[str] = None


class UserWithToken(User):
    token: str


class UserInResponse(RamenSchema):
    user: UserWithToken


class UserByIdInResponse(RamenSchema):
    user: User
