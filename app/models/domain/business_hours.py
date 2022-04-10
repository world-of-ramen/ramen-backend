from typing import Optional

from app.models.domain.ramenmodel import RamenModel


class BusinessHours(RamenModel):
    mo: Optional[str] = None
    tu: Optional[str] = None
    we: Optional[str] = None
    th: Optional[str] = None
    fr: Optional[str] = None
    sa: Optional[str] = None
    su: Optional[str] = None
