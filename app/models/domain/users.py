from typing import Optional

from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.ramenmodel import RamenModel
from app.services import security


class User(RamenModel):
    username: str
    email: str
    bio: str = ""
    image: Optional[str] = None


class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)
