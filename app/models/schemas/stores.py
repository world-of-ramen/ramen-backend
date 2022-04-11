from typing import List
from typing import Optional

from pydantic import BaseModel

from app.models.domain.business_hours import BusinessHours
from app.models.domain.image import Image
from app.models.domain.location import Location
from app.models.domain.social_media import SocialMedia
from app.models.domain.stores import Store
from app.models.schemas.ramenschema import RamenSchema


class StoreInCreate(BaseModel):
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
    status: int = 1


class StoreInUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    image: Optional[Image] = None
    social_media: Optional[SocialMedia] = None
    business_hours: Optional[BusinessHours] = None
    place_id: Optional[str] = None
    location: Optional[Location] = None
    status: Optional[int] = None


class StoreInResponse(RamenSchema):
    store: Store


class StoreListResponse(RamenSchema):
    stores: List[Store]
    total: int
