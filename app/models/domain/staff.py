from typing import Optional

from app.models.domain.rwmodel import HoloModel


class Staff(HoloModel):
    username: str
    account: str
    in_use: bool = True
    dpt: Optional[str] = None
    role: int
    company_name: Optional[str] = None
    email: Optional[str] = None
    company_seal: Optional[str] = None
    boss_seal: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    salary: Optional[str] = None
    salt: str
    hashed_password: Optional[str] = None
    bio: str = ""
    image: Optional[str] = None
