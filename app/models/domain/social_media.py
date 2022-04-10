from typing import Optional

from app.models.domain.ramenmodel import RamenModel


class SocialMedia(RamenModel):
    facebook: Optional[str] = None
