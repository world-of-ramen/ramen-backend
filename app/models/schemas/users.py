from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl

from app.models.domain.users import User
from app.models.schemas.ramenschema import RamenSchema


class UserInLogin(RamenSchema):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UserWithToken(User):
    token: str


class UserInResponse(RamenSchema):
    user: UserWithToken
