from typing import Optional

from app.models.domain.location import Location
from app.models.domain.ramenmodel import RamenModel


class PlaceSummary(RamenModel):
    rating: float
    review_count: int


class PlaceInfo(RamenModel):
    place_id: Optional[str] = None
    location: Optional[Location] = None
