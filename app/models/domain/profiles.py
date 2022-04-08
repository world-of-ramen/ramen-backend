from typing import Optional

from app.models.domain.rwmodel import HoloModel


class Profile(HoloModel):
    username: str
    bio: str = ""
    image: Optional[str] = None
    following: bool = False
