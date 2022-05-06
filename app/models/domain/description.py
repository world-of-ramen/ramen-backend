from typing import Optional

from app.models.domain.ramenmodel import RamenModel


class Description(RamenModel):
    title: Optional[str] = None
    body: Optional[str] = None
