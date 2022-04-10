from typing import Optional

from app.models.domain.ramenmodel import RamenModel


class Image(RamenModel):
    style: Optional[str] = None
    url: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None
    content_type: Optional[str] = None
