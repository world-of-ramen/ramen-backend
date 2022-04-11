from typing import Optional

from app.models.domain.ramenmodel import RamenModel


class Place(RamenModel):
    rating: float
    review_count: int


class PlaceId(RamenModel):
    place_id: Optional[str] = None
