from typing import Optional

from app.models.common import DateTimeModelMixin
from app.models.common import IDModelMixin
from app.models.domain.business_hours import BusinessHours
from app.models.domain.image import Image
from app.models.domain.location import Location
from app.models.domain.ramenmodel import RamenModel
from app.models.domain.social_media import SocialMedia


class Store(IDModelMixin, DateTimeModelMixin, RamenModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    image: Optional[Image] = None
    social_media: Optional[SocialMedia] = None
    business_hours: Optional[BusinessHours] = None
    place_id: Optional[str] = None
    location: Optional[Location] = None
    status: int
