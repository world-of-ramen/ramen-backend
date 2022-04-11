from app.models.domain.ramenmodel import RamenModel


class Place(RamenModel):
    rating: float
    review_count: int
