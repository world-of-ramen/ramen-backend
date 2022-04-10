from typing import Optional

from app.models.domain.ramenmodel import RamenModel


class Profile(RamenModel):
    username: str
    bio: str = ""
    image: Optional[str] = None
    following: bool = False
